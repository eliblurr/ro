from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Category, status_code=201, name='Category')
async def create(payload:schemas.CreateCategory, db:Session=Depends(get_db)):
    return await crud.category.create(payload, db)

@router.get('/', description='', response_model=schemas.CategoryList, name='Category')
@ContentQueryChecker(crud.category.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.category.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Category, name='Category')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.category.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Category, name='Category')
async def update(resource_id:int, payload:schemas.UpdateCategory, db:Session=Depends(get_db)):
    return await crud.category.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Category')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.category.delete(resource_id, db)
