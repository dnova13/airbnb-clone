
import os
import sentry_sdk
from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration


# 
URL = "http://127.0.0.1:8000" # 로컬 루프백 주소, 자기 자신만 접근 가능, 콜백 url 주소

# 0: debug mode , 1 : dev mode(docker), 2: server mode
DEBUG = True
MODE = 0


RDS_HOST = os.getenv('RDS_TEST_HOST')
RDS_NAME = os.getenv('RDS_TEST_NAME')
RDS_USER = os.getenv('RDS_TEST_USER')
RDS_PASSWORD = os.getenv('RDS_TEST_PASSWORD')
RDS_PORT = "5432"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": RDS_HOST,
        "NAME": RDS_NAME,
        "USER": RDS_USER,
        "PASSWORD": RDS_PASSWORD,
        "PORT": RDS_PORT,
    },
}

DJANGO_ADMIN = "xyza/"

