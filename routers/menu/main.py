from fastapi import APIRouter, Depends, File, UploadFile
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import List

router = APIRouter()

@router.post('/', description='', response_model=schemas.Menu, status_code=201, name='Menu')
async def create(payload:schemas.CreateMenu=Depends(schemas.CreateMenu.as_form), images:List[UploadFile]=File(None), db:Session=Depends(get_db)):
    return await crud.menu.create(payload, db, images)

@router.get('/', description='', response_model=schemas.MenuList, name='Menu')
@ContentQueryChecker(crud.menu.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.menu.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Menu, name='Menu')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.menu.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Menu, name='Menu')
async def update(resource_id:int, payload:schemas.UpdateMenu, db:Session=Depends(get_db)):
    return await crud.menu.update(resource_id, payload, db)

@router.put('/{resource_id}/meals', description='', name='Menu')
async def add_meal_to_menu(resource_id:int, meal_ids:List[int], db:Session=Depends(get_db)):
    return await crud.add_meal_to_menu(resource_id, meal_ids, db)

@router.delete('/{resource_id}', description='', name='Menu')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.menu.delete(resource_id, db)

@router.delete('/{resource_id}/meals', description='', name='Menu')
async def add_meal_to_menu(resource_id:int, meal_ids:List[int], db:Session=Depends(get_db)):
    return await crud.remove_meal_from_menu(resource_id, meal_ids, db)