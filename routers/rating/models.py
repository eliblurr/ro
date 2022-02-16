from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, String, Float
from sqlalchemy.orm import relationship, validates
from mixins import BaseMethodMixin
from database import Base

class Rating(BaseMethodMixin, Base):
    '''Rating Model'''
    __tablename__ = "ratings"

    title = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('customers.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True, nullable=False)

    @validates('rating')
    def validate_rating(self, key, rating):
        assert 0 <= rating >= 5, 'range should be a float between 0 and 5'
        return rating