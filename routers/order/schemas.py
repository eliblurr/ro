from typing import Optional, List, Union, Callable
from pydantic import BaseModel, conint, validator
from routers.voucher.schemas import Voucher
from routers.table.schemas import Table
from routers.meal.schemas import Meal
import routers.order.models as  m
import datetime, enum

class OrderMealBase(BaseModel):
    meal_id: int
    class Meta:
        model = m.OrderMeal

class CreateOrderMeal(OrderMealBase):
    quantity: conint(ge=1) = 1 # use to iterate over number of order meals to create with given id
    order_id: Optional[int]

class UpdateOrderMeal(BaseModel):
    order_id: Optional[int]
    status: Optional[m.OrderMealState]
    class Meta:
        model = m.OrderMeal

class UpdateOrCreateOrderMeal(OrderMealBase):
    meal_id:Optional[int]=0
    quantity: Optional[conint(ge=1)]
    status: Optional[m.OrderMealState]

class OrderMeal(BaseModel):
    id:int
    meal: Meal
    status: m.OrderMealState

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    class Meta:
        model = m.Order

class CreateOrder(OrderBase):
    table_id: Optional[int]
    voucher_id: Optional[int]
    restaurant_id:Optional[int]
    meals: List[UpdateOrCreateOrderMeal]

    class Config:
        orm_mode = True

    @validator('restaurant_id')
    def passwords_match(cls, v, values, **kwargs):
        if values['table_id']:
            return None
        if not(v) and not(values['table_id']):
            raise ValueError('table_id and restaurant_id cannot both be empty')
        return v

class UpdateOrder(OrderBase):
    voucher_id: Optional[int]
    status: Optional[m.OrderState]
    meals: Optional[List[CreateOrderMeal]]

    class Meta:
        model = m.Order

class Order(OrderBase):
    id: int
    order_code: str
    restaurant_id: int
    status: m.OrderState
    table: Optional[Table]
    voucher: Optional[Voucher]
    meals: List[OrderMeal] = []
    amount_paid: Optional[float]
    formatted_total: Callable[str, None]
    currency_symbol: Callable[str, None]
    currency: Callable[str, None]
    total: float

    @validator('currency')
    def get_currency(cls, v):
        return v()
    
    @validator('formatted_total')
    def format_total(cls, v):
        return v()
    
    @validator('currency_symbol')
    def get_currency_symbol(cls, v):
        return v()
    
    class Config:
        orm_mode = True

class OrderList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Order]