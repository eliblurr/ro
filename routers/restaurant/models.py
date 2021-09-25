from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from routers.users.accounts.models import User
from routers.voucher.models import Voucher
from routers.table.models import Table
from routers.media.models import Image
from routers.menu.models import Menu
from routers.meal.models import Meal
from constants import PHONE, EMAIL
from mixins import BaseMixin
from database import Base
import re

class Restaurant(BaseMixin, Base):
    '''Restaurant Model'''
    __tablename__ = "restaurants"

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    postal_address = Column(String, nullable=True)
    street_address = Column(String, nullable=True)
    digital_address = Column(String, nullable=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    city = relationship('City', back_populates="restaurants")
    images = relationship('Image', uselist=True, cascade="all, delete")
    vouchers = relationship('Voucher', uselist=True, cascade="all, delete")
    meals = relationship('Meal', back_populates="restaurant", cascade="all, delete")
    users = relationship('User', back_populates="restaurant", cascade="all, delete")
    orders = relationship('Order', back_populates="restaurant", cascade="all, delete")
    tables = relationship('Table', back_populates="restaurant", uselist=True, cascade="all, delete")
    menus = relationship('Menu', secondary='restaurant_menus', backref='restaurant', lazy='dynamic')

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