from routers.voucher.schemas import Voucher
from routers.meal.schemas import Meal
from typing import Optional, List
from pydantic import BaseModel
import datetime

# meals = relationship('OrderMeal', uselist=True)
# voucher = relationship('Voucher', uselist=False)
# table_id = Column(Integer, ForeignKey('tables.id'))
# # order_code = Column(String, nullable=False, default=gen_code)
# status = Column(Enum(OrderState), default=OrderState.active, nullable=False) 
# total = column_property(
#     select(func.sum(OrderMeal.sub_total)).
#     where(and_(
#         OrderMeal.status==OrderMealState.served, OrderMeal.order_id==id
#     )).correlate_except(OrderMeal).scalar_subquery()
# )    
# total_to_pay = column_property(total-voucher.discount(total))


class OrderBase(BaseModel):
    status: Optional[bool]

class CreateOrder(OrderBase):
    table_id: int

class UpdateOrder(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
    restaurant_id: Optional[int]

class Order(OrderBase):
    id: int
    total: float
    total_to_pay: float
    created: datetime.datetime
    updated: datetime.datetime
    voucher: Optional[Voucher]
    meals: Optional[List[Meal]]

    class Config:
        orm_mode = True

class OrderList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Order]