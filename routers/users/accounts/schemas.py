from pydantic import BaseModel, validator
from typing import Optional, List, Union
from utils import list_sum, type_2_pow
from routers.users.role.schemas import Role
import datetime
import enum
from pydantic.types import constr


from . import models as m

class UserTypes(str, enum.Enum):
    users = 'users'
    admins = 'admins'
    customers = 'customers'

class CustomerBase(BaseModel):
    phone: str
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    
    class Config:
        orm_mode = True
      
class CreateCustomer(CustomerBase):
    pass
    
class UpdateCustomer(CustomerBase):
    phone: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    permission: Optional[int]
    
class Customer(CustomerBase):
    id: int
    full_name: str
    created: datetime.datetime
    updated: datetime.datetime

class CustomerList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Customer]

class AdminBase(BaseModel):
    email: str
    
    class Config:
        orm_mode = True
      
class CreateAdmin(AdminBase):
    password: str
    permissions: Optional[List[int]]

    _check_perm_ = validator('permissions', allow_reuse=True, each_item=True)(type_2_pow)
    _sum_perm_ = validator('permissions', allow_reuse=True)(list_sum)
    
class UpdateAdmin(BaseModel):
    email: Optional[str]
    permissions: Optional[int]
    password: Optional[constr(min_length=6)]

    class Meta:
        model = m.Admin
    
class Admin(AdminBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

class AdminList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Admin]

class UserBase(BaseModel):
    role_id: int
    restaurant_id: int
    code: Optional[str]
    
    class Config:
        orm_mode = True
      
class CreateUser(UserBase):
    password: str
    permissions: List[int]

    _check_perm_ = validator('permissions', allow_reuse=True, each_item=True)(type_2_pow)
    _sum_perm_ = validator('permissions', allow_reuse=True)(list_sum)
    
class UpdateUser(BaseModel):
    code: Optional[str]
    role_id: Optional[int]
    permission: Optional[int]
    password: Optional[constr(min_length=6)]

    class Meta:
        model = m.User
    
class User(UserBase):
    id: int
    role: Role
    created: datetime.datetime
    updated: datetime.datetime

class UserList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[User]
