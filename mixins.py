from sqlalchemy import Column, Integer, DateTime, Boolean
import datetime

class BaseMixin(object):    
    status = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # __mapper_args__ = {"order_by":id.desc()}

    @classmethod
    def c(cls):
        return [(c.name, c.type.python_type) for c in cls.__table__.columns]