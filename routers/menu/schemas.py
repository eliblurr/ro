from typing import Optional, List, Union
from routers.media.schemas import Image
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
    images: Optional[List[Image]]
    meals: Optional[List[Meal]] = None

class MenuList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Menu]