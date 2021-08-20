from fastapi import APIRouter, Depends, File, UploadFile
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import List

router = APIRouter()

@router.post('/', description='', response_model=schemas.Restaurant, status_code=201, name='Restaurant')
async def create(payload:schemas.CreateRestaurant=Depends(schemas.CreateRestaurant.as_form), images:List[UploadFile]=File(None), db:Session=Depends(get_db)):
    return await crud.restaurant.create(payload, db, images)

@router.get('/', description='', response_model=schemas.RestaurantList, name='Restaurant')
@ContentQueryChecker(crud.restaurant.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.restaurant.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Restaurant, name='Restaurant')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.restaurant.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Restaurant, name='Restaurant')
async def update(resource_id:int, payload:schemas.UpdateRestaurant, db:Session=Depends(get_db)):
    return await crud.restaurant.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Restaurant')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.restaurant.delete(resource_id, db)