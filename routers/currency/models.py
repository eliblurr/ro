from sqlalchemy import Column, String, event, Index, func
from mixins import BaseMixin, FullTextSearchMixin
from money.currency import Currency as C
from database import Base, SessionLocal
import sqlalchemy

class Currency(BaseMixin, FullTextSearchMixin, Base):
    '''Currency Model'''
    __tablename__ = "currencies"

    title = Column(String, unique=True, nullable=False)
    symbol = Column(String, nullable=True, unique=True)

@event.listens_for(Currency.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([Currency(title=currency.value, symbol=None) for currency in C])
    db.commit()