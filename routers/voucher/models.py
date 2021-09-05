from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from utils import gen_code
from database import Base
import enum

class VoucherState(enum.Enum):
    used = 'used'
    active = 'active'
    expired = 'expired'

class Voucher(BaseMixin, Base):
    '''Voucher Model'''
    __tablename__ = "vouchers"

    discount = Column(Float, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    code = Column(String, default=gen_code, nullable=False, unique=True)
    order = relationship('Order', uselist=False, back_populates="voucher")
    status = Column(Enum(VoucherState), default=VoucherState.active, nullable=False) 
