from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..currency.models import Currency
from routers.restaurant.models import Restaurant
from mixins import BaseMixin
from database import Base

class Country(BaseMixin, Base):
    __tablename__ = "countries"
    
    title = Column(String, nullable=False, unique=True)
    currency = relationship('Currency', backref="countries")
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    sub_countries = relationship('SubCountry', backref="country", uselist=True, cascade="all, delete", lazy='dynamic')

class SubCountry(BaseMixin, Base):
    __tablename__ = "subcountries"

    title = Column(String, nullable=False, unique=True)
    postcode = Column(String, nullable=True, unique=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    cities = relationship('City', backref="subcountry", uselist=True, cascade="all, delete", lazy='dynamic')

class City(BaseMixin, Base):
    __tablename__ = "cities"

    title = Column(String, nullable=False, unique=True)
    postcode = Column(String, nullable=True, unique=False)
    subcountry_id = Column(Integer, ForeignKey('subcountries.id'))
    restaurants = relationship('Restaurant', backref="city", uselist=True, cascade="all, delete", lazy='dynamic')