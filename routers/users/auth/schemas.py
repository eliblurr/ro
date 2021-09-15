from pydantic import BaseModel, constr
from typing import Optional, Union
from ..accounts.schemas import *
from ..role.schemas import *
from constants import PHONE, EMAIL

class UserLogin(BaseModel):
    code: str
    password: str

class AdminLogin(BaseModel):
    email: constr(regex=EMAIL)
    password: str

class CustomerLogin(BaseModel):
    phone: constr(regex=PHONE)

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
    