from sqlalchemy import Column, String, Integer, ForeignKey
from routers.restaurant.models import Restaurant
from sqlalchemy.orm import relationship
from ..currency.models import Currency
from mixins import BaseMixin
from database import Base

class Country(BaseMixin, Base):
    __tablename__ = "countries"
    
    title = Column(String, nullable=False, unique=True)
    currency = relationship('Currency', backref="countries")
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    subcountry = relationship('SubCountry', back_populates="country", uselist=True, cascade="all, delete", lazy='dynamic')

class SubCountry(BaseMixin, Base):
    __tablename__ = "subcountries"

    title = Column(String, nullable=False, unique=True)
    postcode = Column(String, nullable=True, unique=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Country', back_populates="subcountry")
    cities = relationship('City', back_populates="subcountry", uselist=True, cascade="all, delete", lazy='dynamic')

class City(BaseMixin, Base):
    __tablename__ = "cities"

    title = Column(String, nullable=False, unique=True)
    postcode = Column(String, nullable=True, unique=False)
    subcountry_id = Column(Integer, ForeignKey('subcountries.id'))
    subcountry = relationship('SubCountry', back_populates="cities")
    restaurants = relationship('Restaurant', backref="city", uselist=True, cascade="all, delete", lazy='dynamic')