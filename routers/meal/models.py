from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from routers.media.models import Image
from mixins import BaseMixin
from database import Base

from sqlalchemy.ext.hybrid import hybrid_property

class Meal(BaseMixin, Base):
    '''Meal Model'''
    __tablename__ = "meals"

    cost = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship('Restaurant', back_populates="meals")
    images = relationship('Image', uselist=True, cascade="all, delete")
    # ratings

    @hybrid_property
    def currency(self):
        return self.restaurant.city.subcountry.country.currency.title

# class MealRating(RatingMixin, Base):
#     '''Meal Rating Model'''
#     __tablename__ = "meal_ratings"
#     p_name, p_table = Meal.__name__.lower(), Meal.__tablename__
#     # a_name, a_table = 'a', 'b' # author

# from sqlalchemy.orm import relationship, column_property

# total = column_property(
#         select(Currency).
#         where(and_(
#             OrderMeal.status==OrderMealState.served, OrderMeal.order_id==id
#         )).correlate_except(OrderMeal).scalar_subquery()
#     )    

# q = select(Country.currency).join(Region).join(City).join(Restaurant).join(Meal).join(Region).where()
