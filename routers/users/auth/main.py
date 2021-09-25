from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from utils import http_exception_detail, create_jwt
from dependencies import get_db, validate_bearer
from services.email import bg_email, Mail
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from services.sms import send_sms
from schedulers import scheduler
from config import settings
from . import schemas, crud
from typing import Union

router = APIRouter()

def verify_auth_payload(usertype:schemas.UserTypes, payload:Union[schemas.UserLogin, schemas.AdminLogin, schemas.CustomerLogin, schemas.RestaurantLogin]):
    case = (
        usertype.value == 'users' and payload.__class__==schemas.UserLogin, 
        usertype.value == 'admins' and payload.__class__==schemas.AdminLogin,
        usertype.value == 'customers' and payload.__class__==schemas.CustomerLogin,
        usertype.value == 'restaurants' and payload.__class__==schemas.RestaurantLogin
    )    
    if not any(case):
        raise HTTPException(status_code=422, detail=http_exception_detail(loc=[usertype,payload.dict()], msg='selected userType mismatch with payload', type="Payload_UserType mismatch"))
    return {'payload':payload, 'usertype':usertype.value}

@router.post('/login', description='', response_model=schemas.LoginResponse, name='Login')
async def authenticate(data=Depends(verify_auth_payload), db:Session=Depends(get_db)):
    func = crud.verify_user if data["usertype"] == "users" else crud.verify_admin if data["usertype"] == "admin" else crud.verify_user if data['usertype']=='admin' else crud.verify_restaurant

    data = {"userType":data["usertype"], "user":await func(data["payload"], db)}

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
    if await crud.is_token_blacklisted(payload.refresh_token, db):
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="refresh_token", msg="token blacklisted", type="BlacklistedToken"))
    if await revoke_token(payload, db):
        data = decode_jwt(data=payload.refresh_token)
        return {
            "access_token":create_jwt(data=data),
            "refresh_token":create_jwt(data=data, timedelta=timedelta(minutes=settings.REFRESH_SESSION_DURATION_IN_MINUTES)),
        }
    raise HTTPException(status_code=400)

@router.post("/current-user", response_model=Union[schemas.Customer, schemas.Admin, schemas.User], name='Current User')
async def get_current_user(payload:dict=Depends(validate_bearer), db:Session=Depends(get_db)):
    case = ( payload.get("user", {}).get("id"), payload.get("userType") )
    if not all(case):
        raise HTTPException(status_code=400, detail=http_exception_detail(loc="Bearer Token", msg="unrecognizable bearer format", type="AlienBearer"))
    return await crud.get_current_user(case[0], case[1], db)

@router.post("/password-reset-code", name='Password Reset Code')
async def request_password_reset_code(background_tasks:BackgroundTasks, payload:schemas.UserCode, db:Session=Depends(get_db)):
    obj = await crud.verify_user_code_add_pass_reset_code(payload, db)
    scheduler.add_job(
        crud.del_code,
        trigger='date',
        kwargs={'_type':'passcode', 'pk':obj[0].user_id},
        id=f'ID-{obj[0].user_id}',
        replace_existing=True,
        run_date=datetime.utcnow() + timedelta(minutes=settings.RESET_PASSWORD_CODE_VALID_DURATION_IN_MINUTES)
    )
    await bg_email(
        background_tasks, 
        mail=Mail(
            recipients=[obj[1]], 
            subject="Password Verification Code", 
            body=f"Code is {obj[0].code}"
        )
    )
    return 'success'

@router.post("/sms-verification-code", description='', name='SMS Verification Code')
async def request_sms_verification_code(phone:schemas.constr(regex=schemas.PHONE), db:Session=Depends(get_db)):
    obj = await crud.verify_phone_add_sms_verification(phone, db)
    scheduler.add_job(
        crud.del_code,
        trigger='date',
        kwargs={'_type':'sms', 'pk':obj.phone},
        id=f'ID-{obj.phone}',
        replace_existing=True,
        run_date=datetime.utcnow() + timedelta(minutes=settings.SMS_CODE_VALID_DURATION_IN_MINUTES)
    )
    if await send_sms(body=obj.code):
        return 'success'
    return 'failed'
