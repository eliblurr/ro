from jwt.exceptions import ExpiredSignatureError, DecodeError
from utils import decode_jwt, http_exception_detail
from fastapi import HTTPException, Depends
from database import SessionLocal
from main import oauth2_scheme

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def validate_bearer(token:str=Depends(oauth2_scheme), db=Depends(get_db)):
    from routers.user.auth.crud import is_token_blacklisted
    try:
        if await is_token_blacklisted(token, db):
            raise HTTPException(status_code=401, detail=http_exception_detail(loc="Bearer <token>", msg="token blacklisted", type="BlacklistedToken"), headers={"WWW-Authenticate": "Bearer"})
        return decode_jwt(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=http_exception_detail(loc="Bearer <token>", msg="token expired", type="ExpiredSignatureError"), headers={"WWW-Authenticate": "Bearer"})
    except DecodeError:
        raise HTTPException(status_code=500, detail=http_exception_detail(loc="Bearer <token>", msg="token decode failed", type="DecodeError"), headers={"WWW-Authenticate": "Bearer"})
    except:
        raise HTTPException(status_code=500, detail=http_exception_detail(loc="Bearer <token>", msg="something went wrong", type="_"), headers={"WWW-Authenticate": "Bearer"})