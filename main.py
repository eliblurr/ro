from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

origins = ["*"]
headers = ["*"]
methods = ["*"]

app = FastAPI(
    redoc_url=None, 
    docs_url=None,
    openapi_url='/openapi.json',
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Restaurant Order API Service",
        version="2.0.0",
        description="API documentation for food ordering service in restaurants",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers,)

app.mount("/static", StaticFiles(directory="static"), name="static")

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