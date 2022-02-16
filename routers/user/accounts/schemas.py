from routers.user.role.schemas import Role
from typing import Optional, List, Union
from pydantic import BaseModel, constr
from constants import PHONE, EMAIL
from . import models as m
import datetime, enum

class AccountTypes(str, enum.Enum):
    users = 'users'
    admins = 'admins'
    customers = 'customers'

class CustomerBase(BaseModel):
    user_name: str
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    phone: constr(regex=PHONE)
    
    class Config:
        orm_mode = True
      
class CreateCustomer(CustomerBase):
    pass
    
class UpdateCustomer(CustomerBase):
    user_name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    phone: Optional[constr(regex=PHONE)]
    
class Customer(CustomerBase):
    id: int
    full_name: str
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True 

class CustomerList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Customer]

class AdminBase(BaseModel):
    email: constr(regex=EMAIL)
    
    class Config:
        orm_mode = True
      
class CreateAdmin(AdminBase):
    password: constr(min_length=6)

class UpdateAdmin(BaseModel):
    email: Optional[str]
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
    
    class Config:
        orm_mode = True
      
class CreateUser(UserBase):
    password: constr(min_length=6)

class UpdateUser(BaseModel):
    role_id: Optional[int]
    code: Optional[constr(min_length=8)]
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