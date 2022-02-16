from fastapi import APIRouter, Depends, File, UploadFile, Request
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List, Union
from . import crud, schemas
import re

router = APIRouter()

@router.post('/', description='', response_model=schemas.Category, status_code=201, name='Category')
async def create(payload:schemas.CreateCategory=Depends(schemas.CreateCategory.as_form), image:UploadFile=File(None), db:Session=Depends(get_db)):
    return await crud.category.create(payload, db, image=image)

@router.get('/', description='', response_model=schemas.CategoryList, name='Category')
@ContentQueryChecker(crud.category.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.category.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Category, name='Category')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.category.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Category, name='Category')
async def update(resource_id:int, payload:schemas.UpdateCategory, db:Session=Depends(get_db)):
    return await crud.category.update(resource_id, payload, db)

@router.put('/{cat_id}/remove-{resource}', description='', name='Category')
@router.put('/{cat_id}/append-{resource}', description='', name='Category')
async def update(cat_id:int, resource:schemas.RelatedResource, resource_ids:List[int], request:Request, db:Session=Depends(get_db)):
    if re.search(r'(remove)', request.url.path):
        return await crud.rem_resource_from_category(cat_id, resource_ids, resource, db)
    return await crud.add_resource_to_category(cat_id, resource_ids, resource, db)
    
@router.delete('/{resource_id}', description='', name='Category')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.category.delete(resource_id, db)
