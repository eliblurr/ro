from babel.numbers import get_territory_currencies, get_currency_symbol, format_currency
from sqlalchemy import Column, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from mixins import BaseMethodMixin
from .schemas import LocaleChoice
from config import LANGUAGE
from database import Base
import datetime

class Locale(BaseMethodMixin, Base):
    __tablename__ = "locales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Enum(LocaleChoice), nullable=False, unique=True)
    restaurants = relationship('Restaurant', back_populates="locale", cascade="all, delete", lazy='dynamic')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    ads = relationship('AD', secondary='ad_locales', back_populates="locales", lazy='dynamic')

    def get_currency(self):
        currency = get_territory_currencies(self.name, start_date=datetime.date.today())
        if currency:
            return currency[0]
        return None

    def get_currency_symbol(self):
        currency = self.get_currency()
        if currency:
            return get_currency_symbol(currency, locale=f'{LANGUAGE}_{self.name}')
        return None

    def format_currency(self, value:float):
        currency = self.get_currency()
        if currency:
            return format_currency(value, currency, locale=f'{LANGUAGE}_{self.name}')
        return value