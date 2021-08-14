from mixins import BaseMixin, ImageMixin, RatingMixin
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from utils import to_tsvector_ix
from database import Base

class Meal(BaseMixin, Base):
    '''Meal Model'''
    __tablename__ = "meals"

    cost = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    images = relationship('MealImage', backref="meal", uselist=True, cascade="all, delete")
    ratings = relationship('MealRating', backref="meal", uselist=True, cascade="all, delete")

class MealImage(ImageMixin, Base):
    '''Meal Image Model'''
    __tablename__ = "meal_images"
    p_name, p_table= Meal.__name__.lower(), Meal.__tablename__

class MealRating(RatingMixin, Base):
    '''Meal Rating Model'''
    __tablename__ = "meal_ratings"
    p_name, p_table = Meal.__name__.lower(), Meal.__tablename__
    # a_name, a_table = 'a', 'b' # author