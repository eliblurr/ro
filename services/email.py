from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel
from fastapi import BackgroundTasks
from typing import List, Optional
# from main import background_tasks
from config import settings
from functools import wraps

background_tasks = BackgroundTasks()

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

class EmailSchema(BaseModel):
    recipients: List[EmailStr]
    subject: Optional[str]
    body: str

def run_process_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if kwargs.get("bg", False)==True:
            return background_tasks.add_task(func(*args, **kwargs))    
        return func(*args, **kwargs)
    return inner

async def a():
    print('s')

import asyncio

@run_process_decorator
def email(*args, **kwargs):
    # asyncio.run(a)
    # payload:EmailSchema, 
    print('ssdsd')

# @app.post("/emailbackground")
# async def send_in_background(background_tasks: BackgroundTasks,
#     email: EmailSchema
#     ):

#     message = MessageSchema(
#         subject="Fastapi mail module",
#         recipients=email.dict().get("email"),
#         body="Simple background task",
#         )

#     fm = FastMail(conf)

#     background_tasks.add_task(fm.send_message,message)

#     return JSONResponse(status_code=200, content={"message": "email has been sent"})


# @celery.task(base=TaskManager, name='email', autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5, 'countdown': 2}, task_time_limit=60) 
# def send_async_email(*args, **kwargs):
#     mail = Mail.parse_raw(kwargs.get('mail'))
#     message = MessageSchema(
#         subject=mail.content.get('subject','No subject'),
#         recipients=mail.email, 
#         body=kwargs.get('template').format(**mail.content),
#         attachments=kwargs.get('files', []),
#         subtype="html"
#     )
#     asyncio.run(fm.send_message(message))
