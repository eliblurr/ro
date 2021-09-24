from pydantic import BaseModel, conint
from typing import Optional, List
import datetime

class PolicyBase(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    pos_index: conint(gt=0)
    metatitle: Optional[str]
    
class CreatePolicy(PolicyBase):
    pass
    
class UpdatePolicy(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    metatitle: Optional[str]
    description: Optional[str]
    pos_index: Optional[conint(gt=0)]

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