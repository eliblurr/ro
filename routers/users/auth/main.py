from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db

router = APIRouter()

def verify_auth_payload(usertype:str, payload:dict):
    pass

@router.post('/login', description='sd', name='Login')
async def authenticate(data=Depends(verify_auth_payload)):
    pass

@router.post("/logout", name='Logout')
async def logout():
    pass

@router.post("/token/refresh", name='Refresh Token')
async def refresh_token():
    pass

@router.post("/token/obtain", name='Obtain Token')
async def refresh_token():
    pass

@router.post("/request-password-reset", name='Email Password Reset')
async def get_current_user(usertype:str):
    pass

@router.get("/current-user", name='Current User')
async def get_current_user():
    pass