from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi import BackgroundTasks
from database import SessionLocal
from schedulers import scheduler
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@app.on_event('startup')
async def startup_event():
    scheduler.start()

@app.on_event('shutdown')
async def shutdown_event():
    scheduler.shutdown()

from urls import *
from routers.currency.models import Base
from routers.restaurant.models import Base
from routers.location.models import Base
from routers.meal.models import Base
from routers.users.accounts.models import Base
from database import engine

@app.post("/init")
def init():  
    Base.metadata.create_all(bind=engine)

    # uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
