from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

origins = ["*"]
headers = ["*"]
methods = ["*"]

app = FastAPI(
    redoc_url='/redoc', 
    docs_url='/docs',
    openapi_url='/openapi.json',
    version="2.0",
    title="Restaurant Order API Service",
    description="API documentation for food ordering service in restaurants",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers,
)

@app.on_event('startup')
async def startup_event():
    # start schedular here
    print('application is ready')

@app.on_event('shutdown')
async def shutdown_event():
    # shutdown schedular here
    print('see you later')

from urls import *

from routers.location.models import Base
from database import engine
Base.metadata.create_all(bind=engine)