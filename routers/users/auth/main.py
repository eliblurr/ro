from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from . import schemas
from typing import Union
from utils import http_exception_detail

router = APIRouter()

def verify_auth_payload(usertype:schemas.UserTypes, payload:Union[schemas.UserLogin, schemas.AdminLogin, schemas.CustomerLogin]):
    case = (
        usertype.value == 'users' and payload.__class__==schemas.UserLogin, 
        usertype.value == 'admins' and payload.__class__==schemas.AdminLogin,
        usertype.value == 'customers' and payload.__class__==schemas.CustomerLogin
    )    
    if not any(case):
        raise HTTPException(status_code=422, detail=http_exception_detail(loc=[usertype,payload.dict()], msg='selected userType mismatch with payload', type="Payload_UserType mismatch"))
    return {'payload':payload, 'usertype':usertype.value}

@router.post('/login', name='Login')
async def authenticate(data=Depends(verify_auth_payload), db:Session=Depends(get_db)):
    if data["usertype"] == "users":
        pass
    if data["usertype"] == "admins":
        pass
    if data["usertype"] == "customers":
        pass
    # add usertype here
    print(data)

@router.post("/logout", name='Logout')
async def logout(payload:schemas.Logout, db:Session=Depends(get_db)):
    pass

@router.post("/token/refresh", description='', response_model=schemas.Token, name='Refresh Token')
async def refresh_token(payload:schemas.RefreshToken, db:Session=Depends(get_db)):
    pass

@router.post("/current-user", response_model=Union[schemas.Customer, schemas.Admin, schemas.User], name='Current User')
async def get_current_user(payload:schemas.AccessToken):
    pass

@router.get("/password-reset-code", name='Password Reset Code')
async def request_password_reset(user_id:int):
    pass

@router.get("/sms-verification-code", name='SMS Verification Code')
async def request_password_reset(customer_id:int):
    pass

# async def get_current_user(data:dict=Depends(validate_bearer), db:Session=Depends(get_db)):
#     pass