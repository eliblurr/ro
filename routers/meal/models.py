from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from routers.rating.models import Rating
from sqlalchemy.orm import relationship
from routers.media.models import Image
from mixins import BaseMixin
from database import Base

class Meal(BaseMixin, Base):
    '''Meal Model'''
    __tablename__ = "meals"
    __table_args__ = (UniqueConstraint('title', 'restaurant_id', name='uix_title_restaurant_fk'),)

    cost = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship('Restaurant', back_populates="meals")
    images = relationship('Image', uselist=True, cascade="all, delete")
    ratings = relationship('Rating', uselist=True, cascade="all, delete")

    @hybrid_property
    def currency(self):
        return self.restaurant.city.subcountry.country.currency.title