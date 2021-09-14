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
    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)

    # __table_args__ = (
    #     CheckConstraint(
    #         """
    #             (
    #                 (meal_id IS NOT NULL AND COALESCE(menu_id, NULL) IS NULL) 
    #             OR  (menu_id IS NOT NULL AND COALESCE(meal_id, NULL) IS NULL) 
    #             ) 
    #             AND COALESCE(meal_id, menu_id) IS NOT NULL
    #         """
    #     , name="ck_rtg_assoc_single_fk_allowed"),
    # )
    # menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)

    @validates('rating')
    def validate_rating(self, key, rating):
        assert 0 <= rating >= 5, 'range should be a float between 0 and 5'
        return address
    