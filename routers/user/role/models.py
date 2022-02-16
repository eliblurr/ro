from sqlalchemy import Column, String, event
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from database import Base

class Role(BaseMixin, Base):
    '''Restaurant Role Model'''
    __tablename__ = "roles"

    description = Column(String, nullable=True)  
    title = Column(String, nullable=False, unique=True)
    users = relationship('User', back_populates="role", uselist=True, cascade="all, delete", lazy='dynamic')

def after_create(target, connection, **kw):
    connection.execute(
        Role.__table__.insert(), [
            {"title":"admin"},
            {"title":"kitchen"},
            {"title":"waiter"},
        ]
    )

event.listen(Role.__table__, "after_create", after_create)