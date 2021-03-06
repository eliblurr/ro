from pydantic import BaseModel, conint
from typing import Optional, List
import datetime

class FAQBase(BaseModel):
    title: str
    description: str
    index: conint(gt=0)
    status: Optional[bool]
    metatitle: Optional[str]
      
class CreateFAQ(FAQBase):
    pass
    
class UpdateFAQ(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]
    index: Optional[conint(gt=0)]
    
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