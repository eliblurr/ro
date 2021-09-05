from routers.currency.schemas import Currency
from typing import Optional, List, Union
from routers.media.schemas import Image
from pydantic import BaseModel
from utils import as_form
import datetime

class MealBase(BaseModel):
    title: str
    cost: float
    description: str
    status: Optional[bool]
    metatitle: Optional[str]

@as_form
class CreateMeal(MealBase):
    pass

class UpdateMeal(BaseModel):
    title: Optional[str]
    cost: Optional[float]
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]

class Meal(MealBase):
    id: int
    images: List[Image]
    created: datetime.datetime
    updated: datetime.datetime
    currency: Union[Currency, None]

    class Config:
        orm_mode = True

class MealList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Meal]