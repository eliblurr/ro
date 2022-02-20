from routers.rating.schemas import RatingBase
from typing import Optional, List, Union, Callable
from pydantic import BaseModel, confloat, validator
from utils import as_form
import datetime

class MealBase(BaseModel):
    title: str
    description: str
    cost: confloat(gt=0)
    status: Optional[bool]
    metatitle: Optional[str]

    class Config:
        orm_mode = True

@as_form
class CreateMeal(MealBase):
    restaurant_id: int

@as_form
class UpdateMeal(BaseModel):
    title: Optional[str]
    cost: Optional[float]
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]

class Meal(MealBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime
    average_rating: Union[float, str, None]
    ratings: List[Union[RatingBase, None]]
    currency_symbol: Callable[str, None]
    formatted_cost: Callable[str, None]
    currency: Callable[str, None]
    image: Union[str, None]

    @validator('currency')
    def get_currency(cls, v):
        return v()
    
    @validator('formatted_cost')
    def format_cost(cls, v):
        return v()
    
    @validator('currency_symbol')
    def get_currency_symbol(cls, v):
        return v()

class MealList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Meal]