from sqlalchemy import Column, String, Integer, ForeignKey, event
from sqlalchemy.orm import relationship, validates
from utils import today_str, async_remove_file
from routers.upload.models import UploadProxy
from constants import PHONE, EMAIL
from mixins import BaseMixin
from database import Base
from ctypes import File
import re

class Restaurant(BaseMixin, UploadProxy, Base):
    '''Restaurant Model'''
    __tablename__ = "restaurants"

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    postal_address = Column(String, nullable=True)
    street_address = Column(String, nullable=True)
    digital_address = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    locale_name = Column(Integer, ForeignKey('locales.name'))
    locale = relationship('Locale', back_populates="restaurants")
    vouchers = relationship('Voucher', uselist=True, cascade="all, delete")
    meals = relationship('Meal', back_populates="restaurant", cascade="all, delete")
    users = relationship('User', back_populates="restaurant", cascade="all, delete")
    orders = relationship('Order', back_populates="restaurant", cascade="all, delete")
    tables = relationship('Table', back_populates="restaurant", uselist=True, cascade="all, delete")
    menus = relationship('Menu', secondary='restaurant_menus', backref='restaurant', lazy='dynamic')
    logo = Column(File(upload_to=f'{today_str()}'), nullable=False)

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

@event.listens_for(Restaurant, 'after_delete')
def receive_after_delete(mapper, connection, target):
    if target.logo:async_remove_file(target.logo)

@event.listens_for(Restaurant.logo, 'set', propagate=True)
def receive_set(target, value, oldvalue, initiator):
    if oldvalue:async_remove_file(oldvalue)