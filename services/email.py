from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from fastapi import UploadFile, File
from typing import List, Optional
from config import settings

fm = FastMail(
    ConnectionConfig(
        MAIL_USERNAME = settings.MAIL_USERNAME,
        MAIL_PASSWORD = settings.MAIL_PASSWORD,
        MAIL_FROM = settings.MAIL_FROM,
        MAIL_PORT = settings.MAIL_PORT,
        MAIL_SERVER = settings.MAIL_SERVER,
        MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
        MAIL_TLS = settings.MAIL_TLS,
        MAIL_SSL = settings.MAIL_SSL,
        USE_CREDENTIALS = settings.USE_CREDENTIALS,
        VALIDATE_CERTS = settings.VALIDATE_CERTS
    )
)

class Mail(BaseModel):
    subject: Optional[str] = settings.DEFAULT_MAIL_SUBJECT
    recipients: List[EmailStr]
    body: str
    
async def email(mail, *args, **kwargs):
    message = MessageSchema(
        subject=mail.subject,
        recipients=mail.recipients, 
        body=mail.body,
        attachments=kwargs.get('attachments', []),
        subtype="html"
    )
    await fm.send_message(message)

async def bg_email(background_tasks, mail, *args, **kwargs):
    background_tasks.add_task(email, mail, *args, **kwargs)