from services.aws import s3_upload, s3_delete
from services.sms import send_sms
from services.email import email
from utils import delete_path
from .queues import get_queue
from rq import Retry

def report_success(job, connection, result, *args, **kwargs):
    print('success')

def report_failure(job, connection, type, value, traceback):
    print('success')

params = {
    'retry':Retry(max=3, interval=[10, 30, 60]),
    'on_success':report_success,
    'on_failure':report_failure
}

def async_send_email(*args, **kwargs):
    q = get_queue('email')
    if q:
        q.enqueue(email,*args, **kwargs, **params)    

def async_s3_upload(*args, **kwargs):
    q = get_queue('file')
    if q:
        q.enqueue(s3_upload,*args, **kwargs, **params)    

def async_s3_delete(*args, **kwargs):
    q = get_queue('file')
    if q:
        q.enqueue(s3_delete,*args, **kwargs, **params)    

def async_delete_path(*args, **kwargs):
    q = get_queue('file')
    if q:
        q.enqueue(delete_path,*args, **kwargs, **params)    

def async_send_sms(*args, **kwargs):
    q = get_queue('sms')
    if q:
        q.enqueue( send_sms,*args, **kwargs, **params )  