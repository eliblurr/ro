from sqlalchemy import Column, String, Integer
from utils import to_tsvector_ix
from mixins import BaseMixin
from database import Base

class FAQ(BaseMixin, Base):
    '''FAQ Model'''
    __tablename__ = "faqs"

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    pos_index = Column(Integer, autoincrement=True, nullable=False, unique=True, index=True)