from typing import Optional, List
from pydantic import BaseModel
from utils import as_form
from enum import Enum
import datetime

class MediaType(str, Enum):
    audio = 'audio'
    images = 'images'
    videos = 'videos'

class ImageBase(BaseModel):
    small: Optional[str]
    detail: Optional[str]
    listquad: Optional[str]
    thumbnail: Optional[str]

    class Config:
        orm_mode = True

@as_form
class CreateImage(BaseModel):
    meal_id: Optional[int]
    menu_id: Optional[int]
    category_id: Optional[int]
    restaurant_id: Optional[int]

class Image(ImageBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime