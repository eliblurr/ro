from typing import Optional, List
from pydantic import BaseModel
import datetime, enum

class VoucherState(str, enum.Enum):
    used = 'used'
    active = 'active'
    expired = 'expired'

class VoucherBase(BaseModel):
    discount: float

import routers.order.models as  m

class CreateVoucher(VoucherBase):
    restaurant_id: int
    # order_id: Optional[int]

    class Meta:
        model = m.Voucher
    
class UpdateVoucher(BaseModel):
    order_id: Optional[int]
    discount: Optional[float]
    restaurant_id: Optional[int]
    status: Optional[VoucherState]

class Voucher(VoucherBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

    class Meta:
        model = m.Voucher

class VoucherList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Voucher]