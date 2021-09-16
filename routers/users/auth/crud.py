from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from cls import CRUD

revoked_tokens = CRUD(models.RevokedToken)
password_reset_codes = CRUD(models.PasswordResetCode)
sms_verication_codes = CRUD(models.SMSVerificationCode)

async def verify_customer(payload:schemas.CustomerLogin, db:Session):
    # user = db.query().filter().first()
    # if not user:
    #     raise HTTPException(status_code=404)
    return
    # users.read(params, db)
    # user = db.query(User).filter(User.email==payload.email).first()
    # if not user:
    #     raise HTTPException(status_code=404)
    # if user.verify_hash(payload.password, user.password):
    # 404 -> 401  
    
async def verify_admin(payload:schemas.AdminLogin, db:Session):
    pass
    
async def verify_user(payload:schemas.UserLogin, db:Session):
    pass

async def revoke_token(payload:schemas.Logout, db:Session):
    pass

async def refresh_token(payload:schemas.RefreshToken, db:Session):
    pass

async def is_token_blacklisted():
    pass

async def get_current_user():
    pass










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