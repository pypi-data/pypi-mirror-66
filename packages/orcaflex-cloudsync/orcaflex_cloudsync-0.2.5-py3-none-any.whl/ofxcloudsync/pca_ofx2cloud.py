"""pca_ofx2cloud.py

This is a post-calculation actions script for OrcaFlex.

It requires a tag on General called FOLDER with a value that can contain only alphanumeric and the following special characters:

! - _ . * ' ( )

"""
from io import BytesIO

import boto3
from boto3.s3.transfer import TransferConfig
from cryptography.fernet import Fernet

from ofxcloudsync import load_sync_ofx, update_progress

s3 = boto3.client('s3')
GB = 1024 ** 3

import os
import threading


class ProgressPercentage(object):

    def __init__(self, model, size):
        self._model = model
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size)
            progress_test = update_progress(percentage, prefix="Uploading sim", for_sysout=False)
            self._model.ReportActionProgress(progress_test)


def Execute(info):
    sync_ofx = load_sync_ofx()
    config = TransferConfig(max_concurrency=sync_ofx.get("mp_threads", 10),
                            multipart_threshold=sync_ofx.get("mp_threshold", 0.5) * GB)
    initial_sim_bytes = info.model.SaveSimulationMem()
    initial_dat_bytes = info.model.SaveDataMem()
    if sync_ofx.get("key_file"):
        with open(sync_ofx['key_file'], 'rb') as kf:
            fn = Fernet(kf.read())
            sim_token = fn.encrypt(bytes(initial_sim_bytes))
            sim_bytes = BytesIO(sim_token)
            dat_token = fn.encrypt(bytes(initial_dat_bytes))
            dat_bytes = BytesIO(dat_token)
    else:
        sim_bytes = BytesIO(initial_sim_bytes)
        dat_bytes = BytesIO(initial_dat_bytes)
    folder = info.model.general.tags.get("FOLDER")
    if folder is None:
        raise Exception("Must specify a folder in general.tags['FOLDER']")
    bucket = sync_ofx.get('bucket')
    print(f"send {info.modelDirectory} to {bucket}/{folder}")
    s3.upload_fileobj(
        sim_bytes, bucket, f"{folder}/{os.path.split(info.modelFileName)[1]}",
        ExtraArgs={'Metadata': {'model_path': info.modelFileName}}, Config=config,
        Callback=ProgressPercentage(info.model, sim_bytes.__sizeof__())
    )
    s3.upload_fileobj(
        dat_bytes, bucket, f"{folder}/{os.path.split(info.modelFileName)[1].replace('.sim', '.dat')}",
        ExtraArgs={'Metadata': {'model_path': info.modelFileName}}, Config=config
    )
