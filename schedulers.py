from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import settings
from pytz import utc

db_url = 'postgresql:'+settings.DATABASE_URL.split(':', 1)[1] # chect database.py for notes

job_defaults = {'coalesce': False, 'max_instances': 3}
jobstores = {'default': SQLAlchemyJobStore(url=db_url)}
# jobstores = {'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)}
executors = {'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc, misfire_grace_time=settings.BACKGROUND_SCHEDULER_MISFIRE_GRACE_TIME_IN_SECONDS)
