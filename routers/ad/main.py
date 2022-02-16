from fastapi import APIRouter, Depends, File, UploadFile, Request
from routers.location.crud import locale
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List, Union
from . import crud, schemas
import re

router = APIRouter()

@router.post('/', description='', response_model=schemas.AD, status_code=201, name='AD')
async def create(payload:schemas.CreateAD=Depends(schemas.CreateAD.as_form), image:UploadFile=File(None), db:Session=Depends(get_db)):
    return await crud.ad.create(payload, db, image=image)

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

@router.put('/{ad_id}/remove-locales', description='', name='AD')
@router.put('/{ad_id}/append-locales', description='', response_model=Union[List[schemas.ADLocale], None], name='AD')
async def update(ad_id:int, locale_ids:List[int], request:Request, db:Session=Depends(get_db)):
    if re.search(r'(remove-locales)$', request.url.path):
        return await crud.rem_locale_from_ad(ad_id, locale_ids, db)
    return await crud.add_locale_to_ad(ad_id, locale_ids, db)

@router.delete('/{resource_id}', description='', name='AD')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.ad.delete(resource_id, db)

@router.get('/{resource_id}/locales', description='', name='AD')
@ContentQueryChecker(locale.model.c(), None)
async def read(resource_id:int, db:Session=Depends(get_db), **params):
    return await crud.ad.read(params, db, related_name='locales', resource_id=resource_id)
