from sqlalchemy import Column, Integer, DateTime, Boolean
import datetime

class BaseMixin(object):
    status = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)