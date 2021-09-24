from routers.media.schemas import Image
from typing import Optional, List, Union
from pydantic import BaseModel
from utils import as_form
import datetime

from routers.meal.schemas import Meal

class MealMenuBase(BaseModel):
    meal:Meal

    class Config:
        orm_mode = True

class MenuBase(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]

    class Config:
        orm_mode = True

@as_form
class CreateMenu(MenuBase):
    restaurant_id: int

class UpdateMenu(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
    restaurant_id: Optional[int]

class Menu(MenuBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime
    # meals: List[Meal] = None
    images: Optional[List[Image]]

class MenuList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Menu]