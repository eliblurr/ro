from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from routers.media.models import Image
from mixins import BaseMixin
from database import Base

class Meal(BaseMixin, Base):
    '''Meal Model'''
    __tablename__ = "meals"

    cost = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    images = relationship('Image', uselist=True, cascade="all, delete")
    # currency = relationship[m:1]->custom join
#     ratings = relationship('MealRating', backref="meal", uselist=True, cascade="all, delete")

# class MealRating(RatingMixin, Base):
#     '''Meal Rating Model'''
#     __tablename__ = "meal_ratings"
#     p_name, p_table = Meal.__name__.lower(), Meal.__tablename__
#     # a_name, a_table = 'a', 'b' # author
