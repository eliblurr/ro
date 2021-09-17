from pydantic import BaseModel, constr
from typing import Optional, Union
from constants import PHONE, EMAIL
from ..accounts.schemas import *
from ..role.schemas import *

class UserCode(BaseModel):
    code: str

class UserLogin(UserCode):
    password: str

class AdminLogin(BaseModel):
    email: constr(regex=EMAIL)
    password: str

class CustomerLogin(BaseModel):
    phone: constr(regex=PHONE)
    code: str 

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: Union[User, Customer, Admin] 

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
    