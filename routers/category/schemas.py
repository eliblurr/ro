from typing import Optional, List
from pydantic import BaseModel, Field
from utils import as_form
import datetime, enum
from routers.menu.schemas import Menu

class CategoryBase(BaseModel):
    title: str
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]

@as_form
class CreateCategory(CategoryBase):
    restaurant_id: Optional[int]

@as_form
class UpdateCategory(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]
    restaurant_id: Optional[int]
    
class Category(CategoryBase):
    id: int
    image: Optional[str]
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class CategoryList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Category]

class RelatedResource(str, enum.Enum):
    meals = 'meals'
    menus = 'menus'

class CategoryMeal(BaseModel):
    meal_id:int
    category_id:int
    meal_id:int = Field(..., gt=0, alias='c_id')

    class Config:
        orm_mode = True

class CategoryMenu(BaseModel):
    category_id:int
    menu_id:int = Field(..., gt=0, alias='c_id')

    class Config:
        orm_mode = True