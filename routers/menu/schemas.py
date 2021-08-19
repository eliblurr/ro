from routers.media.schemas import Image
from typing import Optional, List
from pydantic import BaseModel
from utils import as_form
import datetime

from routers.meal.schemas import Meal

class MenuBase(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]

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
    meals: Optional[List[Meal]]
    images: Optional[List[Image]]

    class Config:
        orm_mode = True

class MenuList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Menu]