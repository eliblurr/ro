from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
from .models import Voucher
import datetime, enum

class VoucherState(str, enum.Enum):
    used = 'used'
    active = 'active'
    expired = 'expired'

class VoucherBase(BaseModel):
    discount: float
    expiry: Optional[float]
    qualified_amount: Optional[float]

    @validator('qualified_amount')
    def qualified_amount_gte_discount(cls, v, values, **kwargs):
        if v:
            assert v>=values['discount'], 'qualified_amount must be greater or equal to discount'
        return v

class CreateVoucher(VoucherBase):
    restaurant_id: Optional[int]

    class Meta:
        model = Voucher
    
class UpdateVoucher(VoucherBase):
    order_id: Optional[int]
    discount: Optional[float]
    restaurant_id: Optional[int]
    status: Optional[VoucherState]
    qualified_amount: Optional[float]
    expiry: Optional[float]

class Voucher(VoucherBase):
    id: int
    code: str
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

    class Meta:
        model = Voucher

class VoucherList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Voucher]