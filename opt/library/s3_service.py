import json
import io
import pickle
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from library.env import ENV

class S3Service():
    def __init__(self):
        self.env = ENV()
        if self.env.app_env == 'local':
            self.s3 = boto3.resource(
                service_name='s3',
                endpoint_url=self.env.endpoint,
                aws_access_key_id=self.env.access_key,
                aws_secret_access_key=self.env.secret_access_key,
                region_name=self.env.region
            )
        else:
            self.s3 = boto3.resource(
                service_name='s3',
            )
        self.bucket = self.s3.Bucket(self.env.bucket)

    def _session(self):
        s = boto3.session.Session(
            region_name=self.env.region
        )
        return s

    def test_ls(self, source_prefix: str) -> str:
        s3_resource = self._session().resource('s3')
        s3_obj = s3_resource.Bucket(self.env.bucket).objects.filter(Prefix=source_prefix)
        return [k.key.replace(source_prefix, '') for k in s3_obj if os.path.splitext(k.key)[1] == '.pkl']

    def test_download_pickle_from_s3(self, source_prefix: str) -> object:
        with io.BytesIO() as data:
            s3 = boto3.resource('s3')
            s3.Bucket(self.env.bucket).download_fileobj(source_prefix, data)
            data.seek(0)
            return pickle.load(data)

    def ls(self, source_prefix: str) -> str:
        return [k.key for k in self.bucket.objects.all() if os.path.splitext(k.key)[1] == '.pkl' ]

    def download(self, source_prefix: str, file_name: str) -> object:
        SAVE_PATH = Path(source_prefix)
        self.bucket.download_file(file_name, str(SAVE_PATH))

    def upload(self, source_prefix: str, file_name: str) -> object:
        SAVE_PATH = Path(source_prefix)
        self.bucket.upload_file(file_name, str(SAVE_PATH))