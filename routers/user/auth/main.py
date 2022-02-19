from redis_queue.tasks import async_send_email, async_send_sms
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db, validate_bearer
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from schedulers import scheduler
from config import settings
from . import schemas, crud
from typing import Union

router = APIRouter()

def verify_auth_payload(usertype:schemas.UserTypes, payload:Union[schemas.UserLogin, schemas.AdminLogin, schemas.CustomerLogin]):
    case = (
        usertype==schemas.UserTypes.users and isinstance(payload, schemas.UserLogin), 
        usertype==schemas.UserTypes.admin and isinstance(payload, schemas.AdminLogin),
        usertype==schemas.UserTypes.customers and isinstance(payload, schemas.CustomerLogin),
    )  
    if not any(case):
        raise HTTPException(status_code=422, detail=http_exception_detail(loc=[usertype,payload.dict()], msg='selected userType mismatch with payload', type="Payload_UserType mismatch"))
    return {'payload':payload, 'usertype':usertype}

@router.post('/login', description='', response_model=schemas.LoginResponse, name='Login')
async def authenticate(data=Depends(verify_auth_payload), db:Session=Depends(get_db)):
    func = crud.verify_user if data["usertype"]==schemas.UserTypes.users else crud.verify_admin if data["usertype"]==schemas.UserTypes.admin else crud.verify_customer     
    user = await func(data["payload"], db)
    data = {"usertype":data["usertype"].value, "id":user.id}
    if data["usertype"]==schemas.UserTypes.users:
        data.update({'role':user.role.title})
    return {
        "access_token":create_jwt(data=data, exp=timedelta(minutes=settings.ACCESS_SESSION_DURATION_IN_MINUTES)),
        "refresh_token":create_jwt(data=data, exp=timedelta(minutes=settings.REFRESH_SESSION_DURATION_IN_MINUTES)),
        "user":user,
    }
    
@router.post("/logout", name='Logout')
async def logout(payload:schemas.Logout, db:Session=Depends(get_db)):
    return await crud.revoke_token(payload, db)

@router.post("/token/refresh", description='', response_model=schemas.Token, name='Refresh Token')
async def refresh_token(payload:schemas.RefreshToken, db:Session=Depends(get_db)):
    if await crud.is_token_blacklisted(payload.refresh_token, db):
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="refresh_token", msg="token blacklisted", type="BlacklistedToken"))
    if await crud.revoke_token(payload, db):
        data = decode_jwt(token=payload.refresh_token)
        return {
            "access_token":create_jwt(data=data),
            "refresh_token":create_jwt(data=data, exp=timedelta(minutes=settings.REFRESH_SESSION_DURATION_IN_MINUTES)),
        }
    raise HTTPException(status_code=400)

@router.post("/current-user", response_model=Union[schemas.Customer, schemas.Admin, schemas.User], name='Current User')
async def get_current_user(payload:dict=Depends(validate_bearer), db:Session=Depends(get_db)):
    if list(payload.keys())!=['usertype', 'id', 'exp']:
        raise HTTPException(status_code=400, detail=http_exception_detail(loc="Bearer Token", msg="unrecognizable bearer format", type="AlienBearer"))
    return await crud.get_current_user(payload.get("id", None), payload.get("usertype", None), db)

@router.post("/send-email-verification-code", name='Email verification code')
async def request_email_verification_code(payload:schemas.EmailOrCode, user_type:schemas.UserTypes, db:Session=Depends(get_db)):
    obj = await crud.verify_email_add_code(payload.emailOrCode, user_type, db)
    scheduler.add_job(
        crud.del_code,
        trigger='date',
        kwargs={'_type':'email', 'pk':obj.email},
        id=f'ID-{obj.email}',
        replace_existing=True,
        run_date=datetime.utcnow() + timedelta(minutes=settings.RESET_PASSWORD_CODE_VALID_DURATION_IN_MINUTES)
    )
    if async_send_email(mail={
        "subject":"Email Verification",
        "recipients":[obj.email],
        "body":f"your verification code is: {obj.code}"
    }):return 200, 'success'
    return 417, 'failed'

@router.post("/send-sms-verification-code", description='', name='SMS Verification Code')
async def request_sms_verification_code(phone:schemas.constr(regex=schemas.PHONE), db:Session=Depends(get_db)):
    obj = await crud.verify_phone_add_code(phone, db)
    scheduler.add_job(
        crud.del_code,
        trigger='date',
        kwargs={'_type':'sms', 'pk':obj.phone},
        id=f'ID-{obj.phone}',
        replace_existing=True,
        run_date=datetime.utcnow() + timedelta(minutes=settings.SMS_CODE_VALID_DURATION_IN_MINUTES)
    )
    if async_send_sms(body=obj.code, to='+'+obj.phone):
        return 200, 'success'
    return 417, 'failed'
