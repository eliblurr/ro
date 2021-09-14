from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Role, status_code=201, name='Role')
async def create(payload:schemas.CreateRole, db:Session=Depends(get_db)):
    return await crud.role.create(payload, db)

@router.get('/', description='', response_model=schemas.RoleList, name='Role')
@ContentQueryChecker(crud.role.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.role.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Role, name='Role')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.role.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Role, name='Role')
async def update(resource_id:int, payload:schemas.UpdateRole, db:Session=Depends(get_db)):
    return await crud.role.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Role')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.role.delete(resource_id, db)