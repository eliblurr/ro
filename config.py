from pydantic import BaseSettings
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

AUDIO_ROOT = os.path.join(MEDIA_ROOT, 'video/')
VIDEO_ROOT = os.path.join(MEDIA_ROOT, 'audio/')
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images/')

IMAGE_URL = f"/{Path(MEDIA_ROOT).resolve().name}/{Path(IMAGE_ROOT).resolve().name}/"
VIDEO_URL = f"/{Path(MEDIA_ROOT).resolve().name}/{Path(VIDEO_ROOT).resolve().name}/"
AUDIO_URL = f"/{Path(MEDIA_ROOT).resolve().name}/{Path(AUDIO_ROOT).resolve().name}/"

SMALL = (400,400)
LISTQUAD = (250,250)
THUMBNAIL = (128, 128)

ORIGINS = ["*"]
HEADERS = ["*"]
METHODS = ["*"]

JWT_ALGORITHM = "HS256"

class Settings(BaseSettings):
    DATABASE_URL: str
    TWILIO_PHONE_NUMBER: str = '+16196584362' 
    ACCESS_SESSION_DURATION_IN_MINUTES: int = 30
    REFRESH_SESSION_DURATION_IN_MINUTES: int = 500
    TWILIO_AUTH_TOKEN: str = '7b6c506ee07337cc3d02536d5119c4b2'
    TWILIO_ACCOUNT_SID: str = 'AC959cbde01aced5669b0121ffea2df117'
    SECRET: str = "eUCcDNVG$rVB6wUK2TjJRWptEN56b3_wQwxRdSq&R76wE6#m8+-A3sm4sKtLdH3hkug@T&@Szg__KjgjhnhyDHFnt%Ru#y8SxW*m=_7f$2uF9CArFq7LtmQqBNuQdTa@KLt@*Y%M24Ry=eUd%R6QsXW3=Z-g!!Rvu#srJ5*#PhbVq@6pyx=R2Jr7VhsYT_QT^j7uLqkqX2%RPnr9SS5RCbt6d!wY&+FQC6=&f37U&f+8JdXf!QV%pB?7V?QSwvrj"

    class Config:
        env_file = ".env"

settings = Settings()