import boto3
from botocore.exceptions import ClientError
import os

from app import SUCCESS, S3_ERROR

from dotenv import load_dotenv
load_dotenv()

bucket = os.environ.get('S3_BUCKET')
region = os.environ.get('AWS_REGION')
access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

print(bucket, region, access_key_id, secret_access_key)

s3_client = boto3.client(service_name='s3',
                         region_name=region,
                         aws_access_key_id=access_key_id,
                         aws_secret_access_key=secret_access_key)


def upload_file(file_name: str, object_name: str = None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        print(file_name, object_name, bucket)
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError:
        return S3_ERROR
    return SUCCESS


def list_backups():
    pass


def restore_backup():
    pass
