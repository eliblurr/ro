from typing import Optional, List
from pydantic import BaseModel
import datetime

class RoleBase(BaseModel):
    title: str
    description: Optional[str]

    class Config:
        orm_mode = True
    
class CreateRole(RoleBase):
    pass
    
class UpdateRole(BaseModel):
    title: Optional[str]
    description: Optional[str]
   
class Role(RoleBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

class RoleList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Role]