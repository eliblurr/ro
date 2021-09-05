from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()
#  
@router.post('/', description='', response_model=schemas.Order, status_code=201, name='Order')
async def create(payload:schemas.CreateOrder, db:Session=Depends(get_db)):
    return await crud.order.create(payload, db)

@router.get('/', description='', response_model=schemas.OrderList, name='Order')
@ContentQueryChecker(crud.order.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.order.read(params, db)

@router.get('/meals', description='', response_model=schemas.OrderList, name='Meals')
@ContentQueryChecker(crud.order_meal.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.order_meal.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Order, name='Order')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.order.read_by_id(resource_id, db)

@router.put('/{resource_id}', description='', response_model=schemas.Order, name='Order')
async def update(resource_id:int, payload:schemas.UpdateOrder, db:Session=Depends(get_db)):
    return await crud.order.update(resource_id, payload, db)

@router.delete('/{resource_id}', description='', name='Order')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.order.delete(resource_id, db)
