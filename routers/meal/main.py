from fastapi import APIRouter, Depends, File, UploadFile
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import List

router = APIRouter()

@router.post('/', description='', response_model=schemas.Meal, status_code=201, name='Meal')
async def create(payload:schemas.CreateMeal=Depends(schemas.CreateMeal.as_form), images:List[UploadFile]=File(None), db:Session=Depends(get_db)):
    return await crud.meal.create(payload, db, images)

@router.get('/', description='', response_model=schemas.MealList, name='Meal')
@ContentQueryChecker(crud.meal.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.meal.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Meal, name='Meal')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.meal.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Meal, name='Meal')
async def update(resource_id:int, payload:schemas.UpdateMeal, db:Session=Depends(get_db)):
    return await crud.meal.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Meal')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.meal.delete(resource_id, db)