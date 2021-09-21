from sqlalchemy import Column, String, Integer
# from utils import to_tsvector_ix
from mixins import BaseMixin
from database import Base

class Policy(BaseMixin, Base):
    '''Policy Model'''
    __tablename__ = "policies"
    
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    pos_index = Column(Integer, autoincrement=True, nullable=False, unique=True, index=True)