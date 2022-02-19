from fastapi import APIRouter, Depends, File, UploadFile, Request
from cls import ContentQueryChecker
from routers.meal.crud import meal
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List, Union
from . import crud, schemas
import re

router = APIRouter()

@router.post('/', description='', response_model=schemas.Menu, status_code=201, name='Menu')
async def create(payload:schemas.CreateMenu=Depends(schemas.CreateMenu.as_form), image:UploadFile=File(None), db:Session=Depends(get_db)):
    return await crud.menu.create(payload, db, image=image)

@router.get('/', description='', response_model=schemas.MenuList, name='Menu')
@ContentQueryChecker(crud.menu.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.menu.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Menu, name='Menu')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.menu.read_by_id(resource_id, db)

@router.get('/{resource_id}/meals', description='', name='AD')
@ContentQueryChecker(meal.model.c(), None)
async def read(resource_id:int, db:Session=Depends(get_db), **params):
    return await crud.menu.read(params, db, related_name='meals', resource_id=resource_id)

@router.patch('/{resource_id}', description='', response_model=schemas.Menu, name='Menu')
async def update(resource_id:int, payload:schemas.UpdateMenu=Depends(schemas.UpdateMenu.as_form), image:UploadFile=File(None), db:Session=Depends(get_db)):
    return await crud.menu.update_2(resource_id, payload, db, image=image)

@router.put('/{menu_id}/remove-meals', description='', name='AD')
@router.put('/{menu_id}/append-meals', description='', name='AD')
async def update(menu_id:int, meal_ids:List[int], request:Request, db:Session=Depends(get_db)):
    if re.search(r'(remove-meals)$', request.url.path):
        return await crud.rem_meal_from_menu(menu_id, meal_ids, db)
    return await crud.add_meal_to_menu(menu_id, meal_ids, db)

@router.delete('/{resource_id}', description='', name='Menu')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.menu.delete_2(resource_id, db)