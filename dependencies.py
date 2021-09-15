from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# from routers.auth_router.crud import is_token_blacklisted
# from fastapi import Header, HTTPException, Depends
# from database import SessionLocal
# from utils import decode_token
# from main import oauth2_scheme
# import jwt, sys

# async def validate_bearer(token:str=Depends(oauth2_scheme), db=Depends(get_db)):
#     pass
#     try:
#         if await is_token_blacklisted(token, db):
#             return False
#         return decode_token(token)
#     except jwt.exceptions.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail='token expired', headers={"WWW-Authenticate": "Bearer"})
#     except jwt.exceptions.DecodeError:
#         raise HTTPException(status_code=401, detail='decode failed', headers={"WWW-Authenticate": "Bearer"})
#     except:
#         raise HTTPException(status_code=401, detail='decode failed', headers={"WWW-Authenticate": "Bearer"})