from sqlalchemy import Column, String, Integer, ForeignKey
from mixins import BaseMixin
from database import Base

class Table(BaseMixin, Base):
    '''Table Model'''
    __tablename__ = "tables"

    number = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))