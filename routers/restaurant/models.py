from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from routers.voucher.models import Voucher
from routers.table.models import Table
from routers.media.models import Image
from routers.menu.models import Menu
from routers.meal.models import Meal
from constants import PHONE, EMAIL
from mixins import BaseMixin
from database import Base

class Restaurant(BaseMixin, Base):
    '''Restaurant Model'''
    __tablename__ = "restaurants"

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    meals = relationship('Meal', back_populates="restaurant", cascade="all, delete")
    images = relationship('Image', uselist=True, cascade="all, delete")
    vouchers = relationship('Voucher', uselist=True, cascade="all, delete")
    menus = relationship('Menu', secondary='restaurant_menus', backref='restaurant', lazy='dynamic')
    tables = relationship('Table', uselist=True, backref='restaurant', cascade="all, delete")
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', back_populates="restaurants")
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    digital_address = Column(String, nullable=True)
    postal_address = Column(String, nullable=True)
    street_address = Column(String, nullable=True)

    @validates('email')
    def validate_email(self, key, value):
        assert re.search(EMAIL, value), 'invalid email format'
        return value

    @validates('phone')
    def validate_phone(self, key, value):
        assert re.search(PHONE, value), 'invalid phone format'
        return value

class RestaurantMenu(Base):
    __tablename__ = "restaurant_menus"

    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), primary_key=True)