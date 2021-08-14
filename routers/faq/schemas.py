from typing import Optional, List
from pydantic import BaseModel
import datetime

class FAQBase(BaseModel):
    title: str
    pos_index: int
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
      
class CreateFAQ(FAQBase):
    pass
    
class UpdateFAQ(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    metatitle: Optional[str]
    pos_index: Optional[int]
    description: Optional[str]
    
class FAQ(FAQBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class FAQList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[FAQ]