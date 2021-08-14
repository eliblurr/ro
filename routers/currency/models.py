from sqlalchemy import Column, String, event, Index, func
from money.currency import Currency as C
from database import Base, SessionLocal
from utils import to_tsvector_ix
from mixins import BaseMixin

import sqlalchemy

class Currency(BaseMixin, Base):
    '''Currency Model'''
    __tablename__ = "currencies"

    title = Column(String, unique=True, nullable=False)
    symbol = Column(String, nullable=True, unique=True)
    __ts_vector__ = to_tsvector_ix('english', 'title', 'symbol')
    __table_args__ = (
        Index(
            'ix_tsv',
            to_tsvector_ix('english', 'title', 'symbol'),
            postgresql_using='gin'
            ),
            Index(
                'idx_person_fts',
                __ts_vector__,
                postgresql_using='gin'
            ),
        )

@event.listens_for(Currency.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([Currency(title=currency.value, symbol=None) for currency in C])
    db.commit()