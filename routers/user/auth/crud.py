from routers.user.accounts import models as a_models
from utils import http_exception_detail, decode_jwt
from routers.restaurant.models import Restaurant
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import HTTPException
from . import models, schemas
from cls import CRUD

async def verify_customer(payload:schemas.CustomerLogin, db:Session):
    customer = db.query(a_models.Customer).filter_by(phone=payload.phone).first()
    if not customer:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="phone", msg="customer not found", type="NotFound"))
    if not db.query(models.SMSVerificationCode).filter_by(phone=customer.phone, code=payload.code).first():
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="code or phone", msg="wrong credentials", type="Unauthorized"))
    return customer

# async def verify_restaurant(payload:schemas.RestaurantLogin, db):
#     restaurant = db.query(Restaurant).filter_by(email=payload.email).first()
#     if not restaurant:
#         raise HTTPException(status_code=404, detail=http_exception_detail(loc="email", msg="restaurant not found", type="NotFound"))
#     if not db.query(models.RestaurantVerificationCode()).filter_by(email=restaurant.email, code=payload.code).first():
#         raise HTTPException(status_code=401, detail=http_exception_detail(loc="code or email", msg="wrong credentials", type="Unauthorized"))
#     return restaurant

async def verify_user(payload:schemas.UserLogin, db:Session):
    user = db.query(a_models.User).filter_by(code=payload.code).first()
    if not user:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="code", msg="user not found", type="NotFound"))
    if user.verify_hash(payload.password, user.password):
        return user
    else:
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="password or code", msg="wrong credentials", type="Unauthorized"))

async def verify_admin(payload:schemas.AdminLogin, db:Session):
    admin = db.query(a_models.Admin).filter_by(code=payload.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="email", msg="admin not found", type="NotFound"))
    if admin.verify_hash(payload.password, admin.password):
        return admin
    else:
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="password or email", msg="wrong credentials", type="Unauthorized"))

async def revoke_token(payload:schemas.Logout, db:Session):
    db.add_all([RevokedToken(jti=token) for token in payload.dict().values()])
    db.commit()
    return 200, 'success'

async def is_token_blacklisted(token:str, db:Session):
    return db.query(models.RevokedToken.id).filter_by(jti=token).first() is not None

async def verify_phone_add_sms_verification(phone:schemas.constr(regex=schemas.PHONE), db:Session):
    customer = db.query(models.Customer).filter_by(phone=payload.phone).first()
    if not customer:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="phone", msg="customer not found", type="Not Found"))
    obj = models.SMSVerificationCode(phone=customer.phone)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

async def verify_admin_user_code_add_pass_reset_code(payload:schemas.UserCode, db:Session):
    user = db.query(a_models.User).filter_by(code=payload.code).first()
    if not user:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="code", msg="user not found", type="Not Found"))
    if not user.role.title.lower()=="admin":
        raise HTTPException(status_code=403, detail=http_exception_detail(loc="role", msg="user not allowed to perform this operation", type="Permission denied"))
    obj = models.PasswordResetCode(user_id=user.id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj, user.restaurant.email

async def get_current_user(id:str, user_type:schemas.UserTypes, db:Session):
    model = models.User if user_type=="users" else models.Admin if user_type=="admin" else models.Customer
    return db.query(model).get(id)

def del_code(_type, pk, db:Session=SessionLocal()):
    code = db.query(models.SMSVerificationCode).get(pk) if _type=='sms' else db.query(models.PasswordResetCode).get(pk) if _type=='pass-reset-code' else None
    if code:
        db.delete(code)
        db.commit()
    return True