import os
from library.exceptions import EnviromentVariableNotfoundException

class GetEnvVal:
    @classmethod
    def region(cls):
        try:
            AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
        except KeyError as e:
            raise EnviromentVariableNotfoundException(e)
        return AWS_DEFAULT_REGION

    @classmethod
    def bucket(cls):
        try:
            S3_BUCKET = os.environ['S3_BUCKET']
        except KeyError as e:
            raise EnviromentVariableNotfoundException(e)
        return S3_BUCKET

    @classmethod
    def endpoint(cls):
        AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', default='')
        return AWS_S3_ENDPOINT_URL

    @classmethod
    def access_key(cls):
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', default='')
        return AWS_ACCESS_KEY_ID

    @classmethod
    def secret_access_key(cls):
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', default='')
        return AWS_SECRET_ACCESS_KEY

    @classmethod
    def app_env(cls):
        try:
            APP_ENV = os.environ['APP_ENV']
        except KeyError as e:
            raise EnviromentVariableNotfoundException(e)
        return APP_ENV

class ENV:
    def __init__(self):
        self.__region = GetEnvVal.region()
        self.__bucket = GetEnvVal.bucket()
        self.__endpoint = GetEnvVal.endpoint()
        self.__access_key = GetEnvVal.access_key()
        self.__secret_access_key = GetEnvVal.secret_access_key()
        self.__app_env = GetEnvVal.app_env()

    @property
    def region(self):
        return self.__region

    @property
    def bucket(self):
        return self.__bucket

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def access_key(self):
        return self.__access_key

    @property
    def secret_access_key(self):
        return self.__secret_access_key

    @property
    def app_env(self):
        return self.__app_env