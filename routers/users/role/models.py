from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from database import Base

class Role(BaseMixin, Base):
    '''Role Model'''
    __tablename__ = "roles"

    title = Column(String, nullable=False) # unique + restaurant_id
    description = Column(String, nullable=True)  
    users = relationship('User', back_populates="roles", uselist=True, cascade="all, delete", lazy='dynamic')
    permissions = 0