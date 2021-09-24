from pydantic import BaseModel, validator
from utils import list_sum, type_2_pow
from typing import Optional, List
import datetime

class RoleBase(BaseModel):
    title: str

    class Config:
        orm_mode = True
    
class CreateRole(RoleBase):
    permissions: List[int]

    _check_perm_ = validator('permissions', allow_reuse=True, each_item=True)(type_2_pow)
    _sum_perm_ = validator('permissions', allow_reuse=True)(list_sum)
    
class UpdateRole(BaseModel):
    title: Optional[str]
    in_perm: Optional[List[int]] = None
    ex_perm: Optional[List[int]] = None

    _check_ex_perm_ = validator('ex_perm', allow_reuse=True, each_item=True)(type_2_pow)
    _check_in_perm_ = validator('in_perm', allow_reuse=True, each_item=True)(type_2_pow)
    _sum_in_perm_ = validator('in_perm', allow_reuse=True)(list_sum)
    _sum_ex_perm_ = validator('ex_perm', allow_reuse=True)(list_sum)

class Role(RoleBase):
    id: int
    permissions: int
    created: datetime.datetime
    updated: datetime.datetime

class RoleList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Role]