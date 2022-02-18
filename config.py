from pydantic import BaseSettings
from babel import Locale
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = "/media/"
UPLOAD_URL = "/uploads"
UPLOAD_ROOT = os.path.join(BASE_DIR, 'uploads/')

LOG_ROOT = os.path.join(BASE_DIR, 'logs/')

AUDIO_ROOT = os.path.join(UPLOAD_ROOT, 'videos/')
VIDEO_ROOT = os.path.join(UPLOAD_ROOT, 'audio/')
IMAGE_ROOT = os.path.join(UPLOAD_ROOT, 'images/')
DOCUMENT_ROOT = os.path.join(UPLOAD_ROOT, 'documents/')

IMAGE_URL = f"/{Path(UPLOAD_ROOT).resolve().name}/{Path(IMAGE_ROOT).resolve().name}/"
VIDEO_URL = f"/{Path(UPLOAD_ROOT).resolve().name}/{Path(VIDEO_ROOT).resolve().name}/"
AUDIO_URL = f"/{Path(UPLOAD_ROOT).resolve().name}/{Path(AUDIO_ROOT).resolve().name}/"
DOCUMENT_URL = f"/{Path(UPLOAD_ROOT).resolve().name}/{Path(AUDIO_ROOT).resolve().name}/"

SMALL = (400,400)
LISTQUAD = (250,250)
THUMBNAIL = (128, 128)

UPLOAD_EXTENSIONS = {
    "IMAGE":[".jpeg", ".jpg", ".bmp", ".gif", ".png", ".JPEG", ".JPG", ".BMP", ".GIF", ".PNG",],
    "VIDEO":[".mp4", ".avi", ".mpeg"],
    "AUDIO":[".mp3", ".aac", ".wav"],
    "DOCUMENT":[".pdf", ".csv", ".doc", ".docx", ".eot", ".txt", ".xls", ".xlsx"],
}

ORIGINS = ["*"]
HEADERS = ["*"]
METHODS = ["*"]

JWT_ALGORITHM = "HS256"

LANGUAGE = "en"

locale = Locale(LANGUAGE)

class Settings(BaseSettings):
    BASE_URL: str = 'http://localhost'
    DATABASE_URL: str
    ADMIN_EMAIL: str = 'admin@admin.com'
    TWILIO_PHONE_NUMBER: str = '+16196584362'
    SMS_CODE_VALID_DURATION_IN_MINUTES: int = 5
    ACCESS_SESSION_DURATION_IN_MINUTES: int = 30
    REFRESH_SESSION_DURATION_IN_MINUTES: int = 500
    RESET_PASSWORD_CODE_VALID_DURATION_IN_MINUTES: int = 5
    TWILIO_AUTH_TOKEN: str = '7b6c506ee07337cc3d02536d5119c4b2'
    TWILIO_ACCOUNT_SID: str = 'AC959cbde01aced5669b0121ffea2df117'
    API_KEY: str = '_7f$2uF9CArFq7LtmQqBNuQdTa@KLt@*Y%M24Ry=eUd%R6QsXW3=Z-g!!Rvu#srJ5*#PhbV'
    SECRET: str = "eUCcDNVG$rVB6wUK2TjJRWptEN56b3_wQwxRdSq&R76wE6#m8+-A3sm4sKtLdH3hkug@T&@Szg__KjgjhnhyDHFnt%Ru#y8SxW*m=_7f$2uF9CArFq7LtmQqBNuQdTa@KLt@*Y%M24Ry=eUd%R6QsXW3=Z-g!!Rvu#srJ5*#PhbVq@6pyx=R2Jr7VhsYT_QT^j7uLqkqX2%RPnr9SS5RCbt6d!wY&+FQC6=&f37U&f+8JdXf!QV%pB?7V?QSwvrj"
    MAIL_USERNAME: str = "a9f521690f65a4"
    MAIL_PASSWORD: str = "11480b2eec8121"
    MAIL_FROM: str = "elisegb-49cabc@inbox.mailtrap.io"
    MAIL_PORT: int = 2525
    MAIL_SERVER: str = "smtp.mailtrap.io"
    MAIL_FROM_NAME: str = "ROv1"
    MAIL_TLS: bool = False
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DEFAULT_MAIL_SUBJECT: str = "SOME DEFAULT SUBJECT HERE"

    USE_S3: bool = True
    APS_COALESCE: bool = False
    APS_MAX_INSTANCES: int = 20
    APS_MISFIRE_GRACE_TIME: int = 4
    APS_THREAD_POOL_MAX_WORKERS: int = 20
    APS_PROCESS_POOL_MAX_WORKERS: int = 15
    AWS_ACCESS_KEY_ID: str = "AKIAQFCNVCREKTZTA2V2"
    AWS_SECRET_ACCESS_KEY: str = "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"
    AWS_DEFAULT_ACL: str = "public-read"
    AWS_STORAGE_BUCKET_NAME: str = "asset-dev-1990"
    AWS_S3_OBJECT_CACHE_CONTROL: str = "max-age=86400"

    REDIS_HOST:str = "127.0.0.1"
    REDIS_PORT:str = "6379"
    REDIS_PASSWORD:str = ""
    REDIS_USER:str = ""
    REDIS_NODE:str = "0"
    REDIS_URL:str=f"redis://{REDIS_USER}@{REDIS_PASSWORD}:{REDIS_HOST}/{REDIS_PORT}/{REDIS_NODE}"

    class Config:
        env_file = ".env"

settings = Settings()

AWS_S3_CUSTOM_DOMAIN = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': settings.AWS_S3_OBJECT_CACHE_CONTROL}

try:
    if not settings.USE_S3:
        if not os.path.isdir(UPLOAD_ROOT):
            os.mkdir(UPLOAD_ROOT)

        if not os.path.isdir(AUDIO_ROOT):
            os.mkdir(AUDIO_ROOT)

        if not os.path.isdir(VIDEO_ROOT):
            os.mkdir(VIDEO_ROOT)

        if not os.path.isdir(IMAGE_ROOT):
            os.mkdir(IMAGE_ROOT)

        if not os.path.isdir(DOCUMENT_ROOT):
            os.mkdir(DOCUMENT_ROOT)

        if not os.path.isdir(LOG_ROOT):
            os.mkdir(LOG_ROOT)
except:
    pass