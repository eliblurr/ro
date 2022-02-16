from sqlalchemy import Column, String, Integer
from mixins import BaseMixin
from database import Base

class Policy(BaseMixin, Base):
    '''Policy Model'''
    __tablename__ = "policies"
    
    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    index = Column(Integer, autoincrement=True, nullable=False, unique=True, index=True)