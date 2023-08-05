"""pca_ofx2cloud.py

This is a post-calculation actions script for OrcaFlex.

It requires a tag on General called FOLDER with a value that can contain only alphanumeric and the following special characters:

! - _ . * ' ( )

"""
import os
from io import BytesIO

import boto3
from boto3.s3.transfer import TransferConfig
from cryptography.fernet import Fernet

from ofxcloudsync import load_sync_ofx

s3 = boto3.client('s3')
GB = 1024 ** 3
config = TransferConfig(max_concurrency=5, multipart_threshold=5 * GB)


def Execute(info):
    sync_ofx = load_sync_ofx()
    initial_bytes = info.model.SaveSimulationMem()
    if sync_ofx.get("key_file"):
        with open(sync_ofx['key_file'], 'rb') as kf:
            fn = Fernet(kf.read())
            token = fn.encrypt(bytes(initial_bytes))
            model_bytes = BytesIO(token)
    else:
        model_bytes = BytesIO(initial_bytes)
    folder = info.model.general.tags.get("FOLDER")
    if folder is None:
        raise Exception("Must specify a folder in general.tags['FOLDER']")
    bucket = sync_ofx.get('bucket')
    print(f"send {info.modelDirectory} to {bucket}/{folder}")
    s3.upload_fileobj(
        model_bytes, bucket, f"{folder}/{os.path.split(info.modelFileName)[1]}",
        ExtraArgs={'Metadata': {'model_path': info.modelFileName}}
    )
