from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Table, status_code=201, name='Table')
async def create(payload:schemas.CreateTable, db:Session=Depends(get_db)):
    return await crud.table.create(payload, db)

@router.get('/', description='', response_model=schemas.TableList, name='Table')
@ContentQueryChecker(crud.table.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.table.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Table, name='Table')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.table.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Table, name='Table')
async def update(resource_id:int, payload:schemas.UpdateTable, db:Session=Depends(get_db)):
    return await crud.table.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Table')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.table.delete(resource_id, db)
