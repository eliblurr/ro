from fastapi import FastAPI

origins = ['*']

app = FastAPI(docs_url='/docs')

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