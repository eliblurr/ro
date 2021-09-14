from routers.currency.schemas import CurrencyBase
from routers.rating.schemas import RatingBase
from routers.media.schemas import ImageBase
from typing import Optional, List, Union
from pydantic import BaseModel, confloat
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
    pass

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
    currency: Union[CurrencyBase, None]
    images: List[Union[ImageBase, None]]
    ratings: List[Union[RatingBase, None]]

class MealList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Meal]