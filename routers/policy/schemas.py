from typing import Optional, List
from pydantic import BaseModel
import datetime

class PolicyBase(BaseModel):
    title: str
    pos_index: int
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
    
class CreatePolicy(PolicyBase):
    pass
    
class UpdatePolicy(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    metatitle: Optional[str]
    pos_index: Optional[int]
    description: Optional[str]

class Policy(PolicyBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class PolicyList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Policy]