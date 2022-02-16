from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from routers.ad.crud import ad
from . import crud, schemas
from config import locale

router = APIRouter()

@router.post('/locales', description='', status_code=201, name='Locale')
async def create(payload:schemas.LocaleChoice, db:Session=Depends(get_db)):
    payload = schemas.AddLocale(name=payload.name)
    return await crud.locale.create(payload, db)

@router.get('/locales', description='', status_code=201, name='Locale')
@ContentQueryChecker(crud.locale.model.c(), None)
async def read(moderate:bool=False, db:Session=Depends(get_db), **params):
    data = ['GH']
    if moderate:
        data = {
            k:(v,k in data) for k,v in list(locale.territories.items())[
                params['offset']:params['offset']+params['limit']
            ]
        }
        return {
            'bk_size':locale.territories.__len__(),
            'pg_size':data.__len__(),
            'data':data
        }
    return await crud.locale.read(params, db)

@router.get('/locales/{resource_id}', description='', name='Locale')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.locale.read_by_id(resource_id, db)

@router.delete('/locales/{resource_id}', description='', name='Locale')
async def create(resource_id:int, db:Session=Depends(get_db)):
    return await crud.locale.delete(resource_id, db)

@router.get('/locales/{resource_id}/{resource}', description='', name='Location-ADs')
@ContentQueryChecker(ad.model.c(), None)
async def read(resource_id:int, resource:schemas.RelatedResource, db:Session=Depends(get_db), **params):
    return await crud.locale.read(params, db, related_name=resource.value, resource_id=resource_id)