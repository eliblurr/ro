from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from utils import http_exception_detail, create_jwt
from dependencies import get_db, validate_bearer
from services.email import bg_email, Mail
from sqlalchemy.orm import Session
from services.sms import send_sms
from schedulers import scheduler
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
    await bg_email(
        background_tasks, 
        mail=Mail(
            recipients=["a@A.com"], 
            subject="sd", 
            body="as"
        )
    )
    return 'success'

@router.get("/sms-verification-code", description='', name='SMS Verification Code')
async def request_sms_verification_code(phone:schemas.constr(regex=schemas.PHONE), db:Session=Depends(get_db)):
    code = await crud.verify_phone_add_sms_verification(phone, db)
    if await send_sms(body=code):
        return 'success'
    return 'failed'

# scheduler.add_job(delete_password_reset_code, trigger='date', kwargs={'id':new_code.id}, id=f'ID{new_code.id}', replace_existing=True, run_date=datetime.datetime.utcnow()+datetime.timedelta(minutes=settings.RPS_DURATION_IN_MINUTES))
# 1. check if user is admin else 403
# 2. get user restaurant email
# 3. send verification to code to restaurant email
# 4. store in table
# 5. return success
# 6. set expiration time with apscheduler [both]