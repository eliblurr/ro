from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List, Union
from . import crud, schemas

router = APIRouter()

async def model(model:schemas.Model):
    return crud.country if model is schemas.Model.country \
    else crud.subcountry if model is schemas.Model.country \
    else crud.city

async def pair(payload:Union[schemas.Country,], model=Depends(model)):
    if model and payload:
        return model, payload,
    return model

@router.post('/{model}', description='')
async def create(pair=Depends(pair), db:Session=Depends(get_db)):
    return await pair[0].create(pair[1], db)

@router.get('/{model}', description='')
async def read(model=Depends(model), search:str=None, value:str=None, skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    return await model.read(db, search, value, skip, limit)

@router.get('/{model}/{id}', description='')
async def read_by_id(id:int, model=Depends(model), db:Session=Depends(get_db)):
    return await model.read_by_id(id, db)

@router.patch('/{model}/{id}', description='')
async def update(id:int, pair:dict=Depends(pair), db:Session=Depends(get_db)):
    return await pair[0].update(id, pair[1], db)

@router.delete('/{model}/{id}', description='')
async def delete(id:int, model=Depends(model), db:Session=Depends(get_db)):
    return await model.delete(id, db)