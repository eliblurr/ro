from typing import Optional, List
from pydantic import BaseModel
import datetime

class ADBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    
class CreateAD(ADBase):
    pass
    
class UpdateAD(ADBase):
    pass
    
class AD(ADBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class ADList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[AD]