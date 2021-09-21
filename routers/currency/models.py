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

def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([Currency(title=currency.value, symbol=None) for currency in C])
    db.commit()

# event.listen(Currency.__table__, 'after_create', insert_initial_values)

# @event.listens_for(Currency.__table__, 'after_create')
# def insert_initial_values(*args, **kwargs):
#     db = SessionLocal()
#     db.add_all([Currency(title=currency.value, symbol=None) for currency in C])
#     db.commit()

# @event.listens_for(SMSVerificationCode, 'before_insert')
# def delete_existing_value(mapper, connection, target):
#     connection.execute("""DELETE FROM :table WHERE phone=:phone;""",{'table':SMSVerificationCode.__tablename__,'phone':target.phone})