from routers.voucher.schemas import Voucher
from typing import Optional, List, Union
from routers.table.schemas import Table
from routers.meal.schemas import Meal
import routers.order.models as  m
from pydantic import BaseModel
import datetime, enum

class OrderState(str, enum.Enum):
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'

class OrderMealState(str, enum.Enum):
    ready = 'ready'
    served = 'served'
    pending = 'pending'
    preparing = 'preparing'

class CreateOrderMeal(BaseModel):
    meal_id: int
    quantity: int
    order_id: Optional[int]

    class Meta:
        model = m.OrderMeal

class UpdateOrderMeal(BaseModel):
    quantity: Optional[int]
    status: Optional[OrderMealState]
    
class OrderMeal(BaseModel):
    id:int
    meal: Meal
    status: enum.Enum
    quantity: Optional[int]

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: Optional[enum.Enum]

    class Meta:
        model = m.Order

class CreateOrder(OrderBase):
    table_id: int
    voucher_id: Optional[int]
    meals: List[CreateOrderMeal]

    class Config:
        orm_mode = True

class UpdateOrder(BaseModel):
    table_id: Optional[int]
    voucher_id: Optional[int]
    meals: Optional[List[CreateOrderMeal]]

    class Meta:
        model = m.Order

class Order(OrderBase):
    id: int
    total: float
    table: Table
    order_code: str
    status: enum.Enum 
    total: Union[float, None]
    currency: Union[str, None]
    voucher: Optional[Voucher]
    created: datetime.datetime
    updated: datetime.datetime
    amount_paid: Optional[float]
    meals: Optional[List[OrderMeal]]
    
    class Config:
        orm_mode = True

class OrderList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Order]