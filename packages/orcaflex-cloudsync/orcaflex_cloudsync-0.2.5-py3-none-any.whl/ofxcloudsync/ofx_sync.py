import concurrent.futures as cf
import datetime
import os
import sys
import threading
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import List, Union, Generator, Tuple

import boto3
from boto3.s3.transfer import TransferConfig
from cryptography.fernet import Fernet

from ofxcloudsync import load_sync_ofx, update_progress

s3 = boto3.client('s3')


class ProgressPercentage(object):

    def __init__(self, object_name, size):
        self._object_name = object_name
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size)
            text = update_progress(percentage, prefix=f"[{self._object_name}]")
            sys.stdout.write(text)
            sys.stdout.flush()
            # with click.progressbar(length=100,
            #                        label=f'downloading {self._object_name}') as bar:
            #     bar.update(percentage)


def load_fernet(key_file: Union[str, PathLike]) -> Fernet:
    """read key_file into Fernet instance

    :param key_file: str or PathLike of file containing a fernet key
    :return: instance of Fernet
    """
    with open(key_file, 'rb') as keyf:
        return Fernet(keyf.read())


def generate_cloud_objects(bucket: str, folder: str) -> Generator:
    """generates tuples of (key, size, modified) for all objects in bucket with prefix folder

    :param bucket: [str] name of bucket
    :param folder: [str] folder prefix
    :return: generator of (key, size, modified) for every object in folder
    """
    truncated = True
    ct = None  # paging happens with a continuation token
    while truncated:
        if ct is None:
            objs = s3.list_objects_v2(Bucket=bucket, Prefix=folder)
        else:
            objs = s3.list_objects_v2(Bucket=bucket, Prefix=folder, ContinuationToken=ct)
        for o in objs.get('Contents', []):
            yield (o['Key'], o['Size'], o['LastModified'])
        if objs['IsTruncated']:
            ct = objs['NextContinuationToken']
        else:
            truncated = False


def download_object(bucket: str, object_key: str, size: int, modified: datetime.datetime,
                    root_folder: Union[str, PathLike],
                    fernet: Fernet = None, mp_threads: int = 5, mp_threshold: float = 5.0) -> Tuple[str, str]:
    """downloads the object and sets the local file modified time to match the cloud value.
    Will decrypt if fernet is provided.

    :param bucket: [str] name of bucket
    :param object_key: [str] full object key
    :param modified: [datetime] cloud modified value
    :param size: [int] size in bytes of object
    :param root_folder: [str or PathLike] root to sync to
    :param fernet: [Fernet] cryptography interface
    :param mp_thread: [int] number of threads to use in Multipart transfer config (default=5)
    :param mp_threshold: [float] size in GB at which to use multipart transfer (default=5.0)
    :return: [tuple] object_key, local_path
    """
    bytes_io = BytesIO()
    config = TransferConfig(max_concurrency=mp_threads,
                            multipart_threshold=mp_threshold * (1024 ** 3))
    s3.download_fileobj(bucket, object_key, bytes_io, Config=config, Callback=ProgressPercentage(object_key, size))
    if fernet:  # requires decryption
        bytes_io.seek(0)  # go back to the start
        bytes_io = BytesIO(fernet.decrypt(bytes_io.read()))  # decrypt and wrap back in BytesIO
    bytes_io.seek(0)  # get back to the beginning
    local_path = Path(root_folder, object_key)  # join the root and key to get local path
    if not local_path.parent.exists():  # if directories don't exist go and make them
        local_path.parent.mkdir(parents=True)  # full tree mkdir
    with open(local_path, 'wb') as wf:
        wf.write(bytes_io.read())  # write that file
    os.utime(local_path, (modified.timestamp(), modified.timestamp()))  # set the time on the file
    return object_key, str(local_path)


def local_file_object(local_path: Path, root: str) -> Tuple[str, int, datetime.datetime]:
    """make a tuple (key, size, modified) from a local path given folder as the root

    Cloud storage keys are likely to be POSIX style paths (think / not \) and they will be relative the the root
    directory rather than full path.

    :param local_path: [str or PathLike] local file
    :param root: root folder
    :return:
    """
    key = local_path.relative_to(root).as_posix()
    stats = local_path.stat()
    modified = datetime.datetime.fromtimestamp(stats[8]).astimezone(datetime.timezone.utc)
    return (key, stats[6], modified)


def s3sync(bucket: str, root: str, folders: List[str], key_file: str = None, mp_threads: int = 5,
           mp_threshold: float = 5.0) -> None:
    """calls the aws command to sync the bucket to root only including folders

    :param bucket: bucket to be synced
    :param root: path of local folder to sync to
    :param folders: list of folders to sync
    :param mp_thread: [int] number of threads to use in Multipart transfer config (default=5)
    :param mp_threshold: [float] size in GB at which to use multipart transfer (default=5.0)
    :return: None
    """
    for folder in folders:
        cloud_objects = set()  # make an empty set
        for cobj in generate_cloud_objects(bucket, folder):
            cloud_objects.add(cobj)  # populate with all the cloud objects
        if not cloud_objects:  # if there is nothing in this folder on cloud then move on
            continue
        local_objects = set()  # another empty set
        local_file_paths = Path(root, folder).rglob('*')  # get all files in the folder
        with cf.ThreadPoolExecutor(max_workers=10) as ex:  # concurrency as a medium of exchange
            f_fileobj = [ex.submit(local_file_object, lp, root) for lp in local_file_paths]  # make some futures
            for fo in cf.as_completed(f_fileobj):  # go through them as they get done
                local_objects.add(fo.result())  # add to the set

        # at this point we have all the files on the cloud and all the local files
        # we can use simple set logic to find out what needs syncing
        to_sync = cloud_objects.difference(local_objects)
        if key_file:  # encyptoconcurrency
            fn = load_fernet(key_file)
        else:
            fn = None

        # go and down load all those files then and if needed decrypt them
        with cf.ThreadPoolExecutor(max_workers=10) as ex:  # FIAT concurrancy
            f_syncs = [ex.submit(download_object, bucket, key, s, m, root, fn, mp_threads, mp_threshold) for (key, s, m)
                       in
                       to_sync]
            for synced in cf.as_completed(f_syncs):
                src, dest = synced.result()
                print(f"synced {src} to {dest}")


def run_local_sync() -> None:
    """load a config file and call s3sync

    :param config_file_path: path of config file
    :return: None
    """
    config = load_sync_ofx()
    # get multipart config from the config or defaults
    max_concurrency = config.get("mp_threads", 10)
    multipart_threshold = config.get("mp_threshold", 0.5)
    s3sync(
        config['bucket'],
        config['root_folder'],
        config['sync'],
        config.get("key_file"),
        max_concurrency,
        multipart_threshold
    )


if __name__ == "__main__":
    run_local_sync()
