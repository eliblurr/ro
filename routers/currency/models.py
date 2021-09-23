from sqlalchemy import Column, String, event, Index, func
from mixins import BaseMixin, FullTextSearchMixin
from money.currency import Currency as C
from database import Base, SessionLocal
import sqlalchemy

class Currency(BaseMixin, FullTextSearchMixin, Base):
    '''Currency Model'''
    __tablename__ = "currencies"
    __ftcols__ = ("title", "symbol")
    
    title = Column(String, unique=True, nullable=False)
    symbol = Column(String, nullable=True, unique=True)

def after_create(target, connection, **kw):
    connection.execute(
        Currency.__table__.insert(), [{"title":C.value} for C in C]
    )

event.listen(Currency.__table__, "after_create", after_create)