from fastapi import APIRouter, Depends, File, UploadFile
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import List

router = APIRouter()

@router.post('/', description='', response_model=schemas.AD, status_code=201, name='AD')
async def create(payload:schemas.CreateAD=Depends(schemas.CreateAD.as_form), images:List[UploadFile]=File(None), db:Session=Depends(get_db)):
    return await crud.ad.create(payload, db, images)

@router.get('/', description='', response_model=schemas.ADList, name='AD')
@ContentQueryChecker(crud.ad.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.ad.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.AD, name='AD')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.ad.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.AD, name='AD')
async def update(resource_id:int, payload:schemas.UpdateAD, db:Session=Depends(get_db)):
    return await crud.ad.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='AD')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.ad.delete(resource_id, db)
