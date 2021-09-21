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
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    TWILIO_PHONE_NUMBER: str = os.getenv('TWILIO_PHONE_NUMBER', '+16196584362')
    SMS_CODE_VALID_DURATION_IN_MINUTES: int = os.getenv('SMS_CODE_VALID_DURATION_IN_MINUTES', 5)
    ACCESS_SESSION_DURATION_IN_MINUTES: int = os.getenv('ACCESS_SESSION_DURATION_IN_MINUTES', 30)
    REFRESH_SESSION_DURATION_IN_MINUTES: int = os.getenv('REFRESH_SESSION_DURATION_IN_MINUTES', 500)
    RESET_PASSWORD_CODE_VALID_DURATION_IN_MINUTES: int = os.getenv("RESET_PASSWORD_CODE_VALID_DURATION_IN_MINUTES", 2)
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", '7b6c506ee07337cc3d02536d5119c4b2')
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", 'AC959cbde01aced5669b0121ffea2df117')
    BACKGROUND_SCHEDULER_MISFIRE_GRACE_TIME_IN_SECONDS: str =os.getenv("BACKGROUND_SCHEDULER_MISFIRE_GRACE_TIME_IN_SECONDS", 15)
    SECRET: str = os.getenv("SECRET", "eUCcDNVG$rVB6wUK2TjJRWptEN56b3_wQwxRdSq&R76wE6#m8+-A3sm4sKtLdH3hkug@T&@Szg__KjgjhnhyDHFnt%Ru#y8SxW*m=_7f$2uF9CArFq7LtmQqBNuQdTa@KLt@*Y%M24Ry=eUd%R6QsXW3=Z-g!!Rvu#srJ5*#PhbVq@6pyx=R2Jr7VhsYT_QT^j7uLqkqX2%RPnr9SS5RCbt6d!wY&+FQC6=&f37U&f+8JdXf!QV%pB?7V?QSwvrj")
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "a9f521690f65a4")
    MAIL_PASSWORD: str = os.getenv(MAIL_PASSWORD, "11480b2eec8121")
    MAIL_FROM: str = os.getenv(MAIL_FROM, "elisegb-49cabc@inbox.mailtrap.io")
    MAIL_PORT: int = os.getenv("MAIL_PORT", 2525)
    MAIL_SERVER: str = os.getenv(MAIL_SERVER, "smtp.mailtrap.io")
    MAIL_FROM_NAME: str = os.getenv(MAIL_FROM_NAME, "ROv1")
    MAIL_TLS: bool = os.getenv("MAIL_TLS", False)
    MAIL_SSL: bool = os.getenv("MAIL_SSL", False)
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", True)
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", True)
    DEFAULT_MAIL_SUBJECT: str = os.getenv("DEFAULT_MAIL_SUBJECT", "SOME DEFAULT SUBJECT HERE")

    class Config:
        env_file = ".env"

settings = Settings()