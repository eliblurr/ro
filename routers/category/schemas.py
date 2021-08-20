from routers.media.schemas import Image
from typing import Optional, List
from pydantic import BaseModel
from utils import as_form
import datetime

class CategoryBase(BaseModel):
    title: str
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]

@as_form
class CreateCategory(CategoryBase):
    restaurant_id: int

class UpdateCategory(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]
    restaurant_id: Optional[int]
    
class Category(CategoryBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime
    images: Optional[List[Image]]

    class Config:
        orm_mode = True

class CategoryList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Category]