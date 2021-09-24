from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from routers.media.models import Image
from routers.meal.models import Meal
from mixins import BaseMixin
from database import Base

class Menu(BaseMixin, Base):
    '''Menu Model'''
    __tablename__ = "menus"
    __table_args__ = (UniqueConstraint('title', 'restaurant_id', name='uix_menu_title_restaurant_fk'),)

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    images = relationship('Image', uselist=True, cascade="all, delete")
    meals = relationship("Meal", secondary='menu_meals', backref='menu')

class MenuMeal(Base):
    __tablename__ = "menu_meals"

    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True)