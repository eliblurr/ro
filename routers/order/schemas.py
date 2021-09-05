from routers.voucher.schemas import Voucher
from routers.meal.schemas import Meal
from typing import Optional, List, Union
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

class UpdateOrderMeal(BaseModel):
    meal_id: int
    quantity: Optional[int]
    status: Optional[OrderMealState]
    
class OrderMeal(BaseModel):
    meal: Meal
    status: OrderMealState
    quantity: Optional[int]

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: Optional[OrderState]

class CreateOrder(OrderBase):
    table_id: int
    voucher_id: Optional[int]
    meals: List[CreateOrderMeal]

class UpdateOrder(BaseModel):
    table_id: Optional[int]
    voucher_id: Optional[int]
    meals: Optional[Union[CreateOrderMeal, UpdateOrderMeal]]

class Order(OrderBase):
    id: int
    total: float
    total_to_pay: float
    created: datetime.datetime
    updated: datetime.datetime
    voucher: Optional[Voucher]
    meals: Optional[List[OrderMeal]]

    class Config:
        orm_mode = True

class OrderList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Order]