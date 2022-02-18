from typing import Optional, List
from pydantic import BaseModel
from utils import as_form
from enum import Enum
import datetime
from .models import UploadType

class UploadBase(BaseModel):
    url: str
    upload_type: Optional[UploadType]

class Upload(UploadBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class UploadList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Upload]


# from routers import Meal as m
# print(Meal)
# objects = {
#     # 'policies':Policy,
#     'meals': 'Meal'
# }
# # from routers.meal.models import Meal

# Object = Enum('Object', {
#     v:v for v in objects.keys()
# })

# from config import UPLOAD_EXTENSIONS

# print(UPLOAD_EXTENSIONS)


