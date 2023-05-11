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

s3_client = boto3.client(service_name='s3',
                         region_name=region,
                         aws_access_key_id=access_key_id,
                         aws_secret_access_key=secret_access_key)


def upload_file(file_name: str, object_name: str = None) -> int:
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError:
        return S3_ERROR
    return SUCCESS


def list_backups() -> int | list:
    try:
        s3_resource = boto3.resource(service_name='s3',
                                     region_name=region,
                                     aws_access_key_id=access_key_id,
                                     aws_secret_access_key=secret_access_key)
        s3_bucket = s3_resource.Bucket(bucket)
        backups = s3_bucket.objects.all()
        backups = sorted(
            backups, key=lambda backup: backup.last_modified, reverse=True)
        return [backup.key for backup in backups]
    except ClientError:
        return S3_ERROR


def restore_backup(object_name: str, file_name: str = None) -> int:
    if file_name is None:
        file_name = os.path.basename(object_name)
    try:
        s3_client.download_file(bucket, object_name, file_name)
        return SUCCESS
    except ClientError:
        return S3_ERROR
