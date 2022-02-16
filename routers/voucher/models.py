from sqlalchemy import Column, String, Float, ForeignKey, Enum, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from utils import gen_code
from database import Base
import enum

class VoucherState(str, enum.Enum):
    used = 'used'
    active = 'active'
    expired = 'expired'

class Voucher(BaseMixin, Base):
    '''Voucher Model'''
    __tablename__ = "vouchers"
    __table_args__ = (CheckConstraint('qualified_amount >= discount', name='check1'),)

    expiry = Column(DateTime)
    discount = Column(Float, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    code = Column(String, default=gen_code, nullable=False, unique=True)
    order = relationship('Order', uselist=False, back_populates="voucher")
    status = Column(Enum(VoucherState), default=VoucherState.active, nullable=False)
    qualified_amount = Column(Float, nullable=True)

    def is_qualified(self, amount):
        if self.status=='active':
            if self.qualified_amount:
                return self.qualified_amount <= amount
            return True
        return False