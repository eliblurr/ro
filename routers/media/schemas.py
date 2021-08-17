from typing import Optional, List
from pydantic import BaseModel
import datetime

class ImageBase(BaseModel):
    small: Optional[str]
    detail: Optional[str]
    listquad: Optional[str]
    thumbnail: Optional[str]

class Image(ImageBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True