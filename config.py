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

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()