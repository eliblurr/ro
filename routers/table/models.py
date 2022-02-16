from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from utils import gen_code
from database import Base

class Table(BaseMixin, Base):
    '''Table Model'''
    __tablename__ = "tables"
    __table_args__ = (UniqueConstraint('code', 'restaurant_id', name='uix_code_restaurant_fk'),)

    orders = relationship("Order", back_populates="table")
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    restaurant = relationship("Restaurant", back_populates="tables")
    code = Column(String, nullable=False, default=gen_code) 