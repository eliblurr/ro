from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint, event
from sqlalchemy.ext.hybrid import hybrid_property
from utils import today_str, async_remove_file
from routers.rating.models import Rating
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from database import Base
from ctypes import File

from typing import Callable, Optional, Any

class Meal(BaseMixin, Base):
    '''Meal Model'''
    __tablename__ = "meals"
    __table_args__ = (UniqueConstraint('title', 'restaurant_id', name='uix_title_restaurant_fk'),)

    cost = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    restaurant = relationship('Restaurant', back_populates="meals")
    ratings = relationship('Rating', uselist=True, cascade="all, delete")
    image = Column(File(upload_to=f'{today_str()}'), nullable=False)

    def currency(self):       
        return self.restaurant.locale.get_currency() 
    
    def currency_symbol(self):
        return self.restaurant.locale.get_currency_symbol()

    def formatted_cost(self):
        return self.restaurant.locale.format_currency(self.cost)

    @hybrid_property
    def average_rating(self):
        ratings = [item.rating for item in self.ratings] 
        if ratings:return sum(ratings)/ratings.__len__()
        else:return 0.0

@event.listens_for(Meal, 'after_delete')
def receive_after_delete(mapper, connection, target):
    if target.image:async_remove_file(target.image)

@event.listens_for(Meal.image, 'set', propagate=True)
def receive_set(target, value, oldvalue, initiator):
    if oldvalue:async_remove_file(oldvalue)