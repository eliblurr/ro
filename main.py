from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from database import SessionLocal
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

app.mount(cfg.MEDIA_URL, StaticFiles(directory=cfg.MEDIA_ROOT), name="media")
app.mount(cfg.STATIC_URL, StaticFiles(directory=cfg.STATIC_ROOT), name="static")

@app.on_event('startup')
async def startup_event():
    # start schedular here
    print('application is ready')

@app.on_event('shutdown')
async def shutdown_event():
    # shutdown schedular here
    print('see you later')

from urls import *
from routers.restaurant.models import Base
from routers.location.models import Base
from routers.meal.models import Base
from routers.users.accounts.models import Base
from database import engine
Base.metadata.create_all(bind=engine)