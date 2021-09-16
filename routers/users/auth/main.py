from fastapi import APIRouter, Depends, HTTPException
from utils import http_exception_detail, create_jwt
from sqlalchemy.orm import Session
from dependencies import get_db
from datetime import timedelta
from config import settings
from . import schemas, crud
from typing import Union

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

@router.post('/login', description='', response_model=schemas.LoginResponse, name='Login')
async def authenticate(data=Depends(verify_auth_payload), db:Session=Depends(get_db)):
    user = await crud.verify_user(data["payload"], db) if data["usertype"] == "users" else await crud.verify_admin(data["payload"], db) \
           if data["usertype"] == "admins" else await crud.verify_user(data["payload"], db) if data["usertype"] == "customers" else None

    data = {"userType":data["usertype"], "user":user}

    return {
        "access_token":create_jwt(data=data),
        "refresh_token":create_jwt(data=data, timedelta=timedelta(minutes=settings.REFRESH_SESSION_DURATION_IN_MINUTES)),
        "user":user,
    }

@router.post("/logout", name='Logout')
async def logout(payload:schemas.Logout, db:Session=Depends(get_db)):
    return await crud.revoke_token(payload, db)

@router.post("/token/refresh", description='', response_model=schemas.Token, name='Refresh Token')
async def refresh_token(payload:schemas.RefreshToken, db:Session=Depends(get_db)):
    pass

@router.post("/current-user", response_model=Union[schemas.Customer, schemas.Admin, schemas.User], name='Current User')
async def get_current_user(payload:schemas.AccessToken, db:Session=Depends(get_db)):
    pass

@router.get("/password-reset-code", name='Password Reset Code')
async def request_password_reset_code(user_id:int, db:Session=Depends(get_db)):
    pass

@router.get("/sms-verification-code", name='SMS Verification Code')
async def request_sms_verification_code(customer_id:int, db:Session=Depends(get_db)):
    # get customer
    # if customer store in db else 404
    # sendsms from services
    # return 200, success
    pass