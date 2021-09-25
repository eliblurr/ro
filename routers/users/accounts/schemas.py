from typing import Optional, List, Union
from pydantic import BaseModel
import datetime
import enum

class UserTypes(str, enum.Enum):
    users = 'users'
    admin = 'admin'
    customers = 'customers'

class CustomerBase(BaseModel):
    phone: str
    full_name: str
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    
    class Config:
        orm_mode = True
      
class CreateCustomer(CustomerBase):
    pass
    
class UpdateCustomer(CustomerBase):
    phone: Optional[str]
    full_name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    permission: Optional[int]
    
class Customer(CustomerBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

class CustomerList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Customer]

class AdminBase(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True
      
class CreateAdmin(AdminBase):
    pass
    
class UpdateAdmin(AdminBase):
    password: Optional[str]
    
class Admin(AdminBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

class AdminList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Admin]

class UserBase(BaseModel):
    code: str
    role_id: int
    restaurant_id: int
    
    class Config:
        orm_mode = True
      
class CreateUser(UserBase):
    password: str
    permission: Optional[int]
    
class UpdateUser(BaseModel):
    code: Optional[str]
    role_id: Optional[int]
    password: Optional[str]
    permission: Optional[int]
    
class User(UserBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

class UserList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[User]
