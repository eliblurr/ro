from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from routers.media.models import Image
from routers.meal.models import Meal
from mixins import BaseMixin
from database import Base

class Category(BaseMixin, Base):
    '''Category Model'''
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint('title', 'restaurant_id', name='uix_title_restaurant_fk'),)
    # unique constraint on coalesce(restaurant_id not null & title) + title
    
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=True)
    images = relationship('Image', uselist=True, cascade="all, delete")
    meals = relationship('Meal', secondary='category_meals', backref='category', lazy='dynamic')

class CategoryMeal(Base):
    '''Category Meal Model'''
    __tablename__ = 'category_meals'

    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)