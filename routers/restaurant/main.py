from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import List

router = APIRouter()

@router.post('/', description='', response_model=schemas.Restaurant, status_code=201, name='Restaurant')
async def create(payload:schemas.CreateRestaurant=Depends(schemas.CreateRestaurant.as_form), image:UploadFile=File(...), db:Session=Depends(get_db)):
    return await crud.restaurant.create(payload, db, image=image)

@router.get('/', description='', response_model=schemas.RestaurantList, name='Restaurant')
@ContentQueryChecker(crud.restaurant.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.restaurant.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Restaurant, name='Restaurant')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.restaurant.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Restaurant, name='Restaurant')
async def update(resource_id:int, payload:schemas.UpdateRestaurant=Depends(schemas.UpdateRestaurant.as_form), image:UploadFile=File(None), db:Session=Depends(get_db)):
    return await crud.restaurant.update_2(resource_id, payload, db, image=image)

@router.delete('/{resource_id}', description='', name='Restaurant')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.restaurant.delete_2(resource_id, db)

@router.get('/{resource_id}/{upload}', description='', name='Restaurant')
async def read(resource_id:int, upload:schemas.Uploads, offset:int=0, limit:int=100, db:Session=Depends(get_db)):
    obj = await crud.restaurant.read_by_id(resource_id, db)
    if not obj:raise HTTPException(status_code=404, detail="restaurant not found")
    if upload.value=="audio":return obj.audio(db, offset, limit)
    elif upload.value=="videos":return obj.videos(db, offset, limit)
    elif upload.value=="images":return obj.images(db, offset, limit)
    elif upload.value=="documents":return obj.documents(db, offset, limit)