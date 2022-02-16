from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Rating, status_code=201, name='Rating')
async def create(payload:schemas.CreateRating, db:Session=Depends(get_db)):
    return await crud.rating.create(payload, db)

@router.get('/', description='', response_model=schemas.RatingList, name='Rating')
@ContentQueryChecker(crud.rating.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.rating.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Rating, name='Rating')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.rating.read_by_id(resource_id, db)

@router.delete('/{resource_id}', description='', name='Rating')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.rating.delete(resource_id, db)