import uuid
import json
import boto3
from datetime import datetime
from django.conf import settings
from botocore.client import Config
from botocore.exceptions import ClientError

from MSRV.apps.utils.enum_type import TypeFileEnum


class UpLoadFileToClone:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UpLoadFileToClone, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        s3 = boto3.client('s3',
                          endpoint_url=settings.MINIO_HOST,
                          aws_access_key_id=settings.MINIO_USER,
                          aws_secret_access_key=settings.MINIO_PASSWORD,
                          config=Config(signature_version='s3v4'))
        self.cloud = s3
        self.create_bucket_and_set_policy(TypeFileEnum.VIDEO.lower())
        self.create_bucket_and_set_policy(TypeFileEnum.IMAGE.lower())

    def create_bucket_and_set_policy(self, bucket_name):
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*"
                    },
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        try:
            # Kiểm tra nếu bucket không tồn tại thì tạo mới
            try:
                self.cloud.head_bucket(Bucket=bucket_name)
                print(f"Bucket '{bucket_name}' đã tồn tại.")
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    self.cloud.create_bucket(Bucket=bucket_name)
                    # Set policy cho bucket
                    self.cloud.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
                    print(f"Đã tạo bucket '{bucket_name}'.")
                else:
                    print(f"Đã xảy ra lỗi: {e}")
                    return
            print(f"Đã áp dụng custom Access Policy cho bucket '{bucket_name}'")
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")

    def upload_file(self, file_obj, type_file, folder):
        file_extension = self.get_file_extension(type_file=type_file)
        if not file_extension:
            return None

        name_object = self.get_name_file(folder=folder, file_extension=file_extension)
        self.cloud.upload_fileobj(file_obj, type_file.lower(), name_object, ExtraArgs={
            'ContentType': file_obj.content_type
        })
        return f"{type_file.lower()}/{name_object}"


    @staticmethod
    def get_file_extension(type_file):
        if type_file == TypeFileEnum.VIDEO.lower():
            return ".webm"
        elif type_file == TypeFileEnum.IMAGE:
            return ".jpg"
        elif type_file == TypeFileEnum.DOCUMENT:
            return ".docx"
        else:
            raise None

    @staticmethod
    def get_name_file(file_extension, folder):
        unique_id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{folder}/{unique_id}_{current_time}{file_extension}"
