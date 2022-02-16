from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import close_all_sessions
from fastapi.staticfiles import StaticFiles
from schedulers import scheduler
from fastapi import FastAPI
import config as cfg

app = FastAPI(
    title="Restaurant Order API Service",
    redoc_url=None, 
    docs_url=None,
    version="1.1.0",
    openapi_url='/openapi.json',)

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins = cfg.ORIGINS,
    allow_methods = cfg.METHODS,
    allow_headers = cfg.HEADERS,)

app.mount(cfg.MEDIA_URL, StaticFiles(directory=cfg.UPLOAD_ROOT), name="upload")
app.mount(cfg.STATIC_URL, StaticFiles(directory=cfg.STATIC_ROOT), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@app.on_event('startup')
async def startup_event():
    scheduler.start()

@app.on_event('shutdown')
async def shutdown_event():
    close_all_sessions()
    scheduler.shutdown()

from urls import *