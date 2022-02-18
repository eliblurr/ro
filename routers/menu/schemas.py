from typing import Optional, List
# from routers.media.schemas import Image
from routers.meal.schemas import Meal
from pydantic import BaseModel
from utils import as_form
import datetime

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

@as_form
class UpdateMenu(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
    restaurant_id: Optional[int]

class Menu(MenuBase):
    id: int
    image: Optional[str]
    created: datetime.datetime
    updated: datetime.datetime
    meals: Optional[List[Meal]] = []

class MenuList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Menu]

class MenuMeal(BaseModel):
    menu_id:int
    meal_id:int

    class Config:
        orm_mode=True