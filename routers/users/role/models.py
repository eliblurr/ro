from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from database import Base

class Role(BaseMixin, Base):
    '''Role Model'''
    __tablename__ = "roles"

    description = Column(String, nullable=True)  
    title = Column(String, nullable=False, unique=True)
    permissions = Column(BigInteger, nullable=False, default=0)
    users = relationship('User', back_populates="role", uselist=True, cascade="all, delete", lazy='dynamic')
    # restaurant_id -> title + restaurant_id IS unique