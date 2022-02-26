from exceptions import NotFoundError, UnacceptableError
from utils import http_exception_detail
from fastapi import APIRouter, Depends, HTTPException
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Order, status_code=201, name='Order')
async def create(payload:schemas.CreateOrder, db:Session=Depends(get_db)):
    payload.meals = crud.verify_order(payload.meals, payload.voucher_id, db)
    return await crud.order.create(payload, db)

@router.get('/', description='', response_model=schemas.OrderList, name='Order')
@ContentQueryChecker(crud.order.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.order.read(params, db)

@router.get('/{resource_id}/meals', description='', response_model=schemas.OrderList, name='Meals')
@ContentQueryChecker(crud.order_meal.model.c(), None)
async def read(resource_id:int, db:Session=Depends(get_db), **params):
    params.update({"order_id":resource_id})
    return await crud.order_meal.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Order, name='Order')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.order.read_by_id(resource_id, db)

@router.patch('/meals/{id}', description='', name='Order Meal')
async def update(id:int, payload:schemas.UpdateOrderMeal, db:Session=Depends(get_db)):
    return await crud.order_meal.update(id, payload, db)

@router.put('/{resource_id}', description='', response_model=schemas.Order, name='Order')
async def update(resource_id:int, payload:schemas.UpdateOrder, db:Session=Depends(get_db)):
    return await crud.order.update(resource_id, payload.copy(exclude={'meals'}), db)

# @router.put('/{order_id}/meals/{meal_id}', description='', response_model=schemas.OrderMeal, name='Order')
# async def update(order_id:int, meal_id:int, payload:schemas.CreateOrderMeal, db:Session=Depends(get_db)):
#     return await crud.order.update(resource_id, payload.copy(exclude={'meals'}), db)

@router.delete('/{resource_id}', description='', name='Order')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.order.delete(resource_id, db)

# @router.delete('/meals/{order_meal_id}', description='', response_model=schemas.OrderMeal, name='Order')
# async def update(order_meal_id:int, db:Session=Depends(get_db)):
#     return await crud.order_meal.delete(order_meal_id, db)
