from utils import http_exception_detail, decode_jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from cls import CRUD

async def verify_customer(payload:schemas.CustomerLogin, db:Session):
    customer = db.query(models.Customer).filter_by(phone=payload.phone).first()
    if not customer:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="phone", msg="customer not found", type="Not Found"))
    if not db.query(models.SMSVerificationCode).filter_by(phone=customer.phone, code=payload.code).first():
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="code or phone", msg="wrong credentials", type="Unauthorized"))
    return customer
    
async def verify_admin(payload:schemas.AdminLogin, db:Session):
    admin = db.query(models.Admin).filter_by(code=payload.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="email", msg="admin not found", type="Not Found"))
    if admin.verify_hash(payload.password, admin.password):
        return admin
    else:
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="password or email", msg="wrong credentials", type="Unauthorized"))
    
async def verify_user(payload:schemas.UserLogin, db:Session):
    user = db.query(models.User).filter_by(code=payload.code).first()
    if not user:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc="code", msg="user not found", type="Not Found"))
    if user.verify_hash(payload.password, user.password):
        return user
    else:
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="password or code", msg="wrong credentials", type="Unauthorized"))

async def revoke_token(payload:schemas.Logout, db:Session):
    db.add_all([RevokedToken(jti=token) for token in payload.dict().values()])
    db.commit()
    return 'success'

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
    return {"code":obj.code}

async def get_current_user(id:str, user_type:str, db:Session):
    model = models.User if user_type == "users" else models.Admin if user_type == "admin" else models.Customer
    return db.query(model).get(id)

def del_():
    pass
# async def refresh_token(payload:schemas.RefreshToken, db:Session):
#     if await is_token_blacklisted(payload.refresh_token, db):
#         raise HTTPException(status_code=401, detail=http_exception_detail(loc="refresh_toker", msg="token blacklisted", type="BlacklistedToken"))
#     if await revoke_token(payload, db):
#         data = decode_jwt(data=payload.refresh_token)
#         user = await read_user_by_id(data.get('id', 0), db)
#         return {
#             "access_token": utils.create_token(data = {'email':user.email,'id':user.id, 'permissions':user.custom_perm+user.role.permissions}, expires_delta=datetime.timedelta(minutes=settings.TOKEN_DURATION_IN_MINUTES)), 
#             "refresh_token": utils.create_token(data = {'id':user.id}, expires_delta=datetime.timedelta(minutes=settings.R_TOKEN_DURATION_IN_MINUTES)), 
#         }
#     raise HTTPException(status_code=400)

# from ..accounts.crud import users, admins, customers
# User
# Admin
# Customer
# users = CRUD(models.User)
# admins = CRUD(models.Admin)
# customers = CRUD(models.Customer)

# if user is None:raise HTTPException(status_code=404, detail=http_exception_detail())
# data:dict, expires_delta:Optional[timedelta]=None

# user = db.query(User).filter(User.email==payload.email).first()
# if not user:
#     raise HTTPException(status_code=404)
# if user.verify_hash(payload.password, user.password):
#     return {
#         "access_token": utils.create_token(data = {'email':payload.email,'id':user.id, 'permissions':user.custom_perm+user.role.permissions}, expires_delta=datetime.timedelta(minutes=settings.TOKEN_DURATION_IN_MINUTES)), 
#         "refresh_token": utils.create_token(data = {'id':user.id}, expires_delta=datetime.timedelta(minutes=settings.R_TOKEN_DURATION_IN_MINUTES)), 
#         "user": user
#     }
# else:
#     raise HTTPException(status_code=401)
# add usertype here
# print(data)
# async def revoke_token(payload:schemas.Token, db:Session):
#     db.add_all([models.RevokedToken(jti=token) for token in list({v for (k,v) in payload.dict().items()}) if token is not None])
#     db.commit()
#     db.close() 
#     return True

# async def refresh_token(payload:schemas.Token, db:Session):
#     if await is_token_blacklisted(payload.refresh_token, db):
#         raise HTTPException(status_code=401)
#     if await revoke_token(payload, db):
#         data = utils.decode_token(data=payload.refresh_token)
#         user = await read_user_by_id(data.get('id', 0), db)
#         return {
#             "access_token": utils.create_token(data = {'email':user.email,'id':user.id, 'permissions':user.custom_perm+user.role.permissions}, expires_delta=datetime.timedelta(minutes=settings.TOKEN_DURATION_IN_MINUTES)), 
#             "refresh_token": utils.create_token(data = {'id':user.id}, expires_delta=datetime.timedelta(minutes=settings.R_TOKEN_DURATION_IN_MINUTES)), 
#         }
#     raise HTTPException(status_code=400)

# async def is_token_blacklisted(token:str, db:Session):
#     return bool(db.query(models.RevokedToken).filter(models.RevokedToken.jti==token).first())

# async def request_password_reset(payload:schemas.Email, db:Session, background_tasks):
#     user = db.query(User).filter(User.email==payload.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail='user not found')
#     new_code = models.PasswordResetCode(user_id=user.id, code=models.PasswordResetCode.generate_code())
#     code = db.query(models.PasswordResetCode).filter(models.PasswordResetCode.user_id==user.id).first()    
#     if code:
#         db.delete(code)
#         db.flush()
#     db.add(new_code)
#     db.commit()
#     db.refresh(new_code)
#     scheduler.add_job(delete_password_reset_code, trigger='date', kwargs={'id':new_code.id}, id=f'ID{new_code.id}', replace_existing=True, run_date=datetime.datetime.utcnow()+datetime.timedelta(minutes=settings.RPS_DURATION_IN_MINUTES))
#     try:
#         send_async_email.delay(mail=Mail(email=[f'{payload.email}'], content={'code':new_code.code, 'name':f'{user.info.first_name} {user.info.last_name}', 'duration':f'{settings.RPS_DURATION_IN_MINUTES} minutes'}).json(), template=email('password-reset'))
#     except:      
#         eLogger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
#         return False
#     return True

# async def get_current_user(data:dict, db:Session):
#     return await read_user_by_id(data.get('id'), db)

# def delete_password_reset_code(id:int, db:Session=SessionLocal()):
#     code = db.query(models.PasswordResetCode).filter(models.PasswordResetCode.id==id).first()
#     if code:
#         db.delete(code)
#     db.commit()
#     return True