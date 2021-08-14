from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Policy, status_code=201, name='Policy')
async def create(payload:schemas.CreatePolicy, db:Session=Depends(get_db)):
    return await crud.policy.create(payload, db)

@router.get('/', description='', response_model=schemas.PolicyList, name='Policy')
@ContentQueryChecker(crud.policy.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.policy.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Policy, name='Policy')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.policy.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Policy, name='Policy')
async def update(resource_id:int, payload:schemas.UpdatePolicy, db:Session=Depends(get_db)):
    return await crud.policy.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Policy')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.policy.delete(resource_id, db)
