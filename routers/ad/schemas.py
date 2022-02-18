from typing import Optional, List, Union
from pydantic import BaseModel
from utils import as_form
import datetime

class ADLocale(BaseModel):
    ad_id:int
    locale_id:int

    class Config:
        orm_mode = True

class ADBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

@as_form
class CreateAD(ADBase):pass

@as_form
class UpdateAD(ADBase):pass
    
class AD(ADBase):
    id: int
    image:Optional[str]
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class ADList(BaseModel):
    bk_size: int
    pg_size: int
    data: Union[List[AD], list]