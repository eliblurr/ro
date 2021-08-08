from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Currency, status_code=201, name='Currency')
async def create(payload:schemas.CreateCurrency, db:Session=Depends(get_db)):
    return await crud.currency.create(payload, db)

@router.get('/', description='', response_model=schemas.CurrencyList, name='Currencies')
@ContentQueryChecker(crud.currency.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.currency.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Currency, name='Currency')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.currency.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Currency, name='Currency')
async def update(resource_id:int, payload:schemas.UpdateCurrency, db:Session=Depends(get_db)):
    return await crud.currency.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Currency')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.currency.delete(resource_id, db)
