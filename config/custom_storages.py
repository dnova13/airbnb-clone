from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static/"
    file_overwrite = False  # 파일을 덮어씌우지 않음


class UploadStorage(S3Boto3Storage):
    location = "uploads/"
