from routers.voucher.schemas import Voucher
from typing import Optional, List, Union
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

    class Meta:
        model = m.OrderMeal

class UpdateOrderMeal(BaseModel):
    meal_id: int
    quantity: Optional[int]
    status: Optional[OrderMealState]
    
class OrderMeal(BaseModel):
    meal: Meal
    # status: Optional[str] = None
    # status: OrderMealState
    quantity: Optional[int]

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    pass
    # status: Optional[OrderState]

class CreateOrder(OrderBase):
    table_id: int
    voucher_id: Optional[int]
    meals: List[CreateOrderMeal]
    # restaurant_id: int

    class Config:
        orm_mode = True

    class Meta:
        model = m.Order

class UpdateOrder(BaseModel):
    table_id: Optional[int]
    voucher_id: Optional[int]
    meals: Optional[Union[CreateOrderMeal, UpdateOrderMeal]]

class Order(OrderBase):
    id: int
    total: float
    currency: Union[str, None]
    total: Union[float, None]
    created: datetime.datetime
    updated: datetime.datetime
    # restaurant_id: Optional[int]
    # table_restaurant: Optional[int]
    # total_to_pay: Union[float, None]
    voucher: Optional[Voucher]
    # meals: Optional[List[OrderMeal]]
    # status: OrderState = OrderState.active

    class Config:
        orm_mode = True

class OrderList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Order]