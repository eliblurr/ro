from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint, event
from utils import today_str, async_remove_file
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from database import Base
from ctypes import File

class Menu(BaseMixin, Base):
    '''Menu Model'''
    __tablename__ = "menus"
    __table_args__ = (UniqueConstraint('title', 'restaurant_id', name='uix_menu_title_restaurant_fk'),)

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    image = Column(File(upload_to=f'{today_str()}'), nullable=True)
    meals = relationship("Meal", secondary='menu_meals', backref='menu')

class MenuMeal(Base):
    __tablename__ = "menu_meals"

    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True)

@event.listens_for(Menu, 'after_delete')
def receive_after_delete(mapper, connection, target):
    if target.image:async_remove_file(target.image)

@event.listens_for(Menu.image, 'set', propagate=True)
def receive_set(target, value, oldvalue, initiator):
    if oldvalue:async_remove_file(oldvalue)