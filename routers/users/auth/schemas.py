from routers.restaurant.schemas import Restaurant
from pydantic import BaseModel, constr
from typing import Optional, Union
from constants import PHONE, EMAIL
from ..accounts.schemas import *
from ..role.schemas import *
import enum

class UserTypes(str, enum.Enum):
    users = 'users'
    admin = 'admin'
    customers = 'customers'
    restaurants = 'restaurants'

class UserCode(BaseModel):
    code: str

class UserLogin(UserCode):
    password: str

class AdminLogin(BaseModel):
    email: constr(regex=EMAIL)
    password: str

class CustomerLogin(UserCode):
    phone: constr(regex=PHONE)

class RestaurantLogin(UserCode):
    email: constr(regex=EMAIL)

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: Union[User, Customer, Admin, Restaurant] 

    class Config:
        orm_mode = True

class AccessToken(BaseModel):
    access_token: str

class RefreshToken(BaseModel):
    refresh_token: str

class Logout(BaseModel):
    access_token: str
    refresh_token: str

class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    