from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import Union

router = APIRouter()

@router.post('/countries', description='', response_model=schemas.Country, status_code=201, name='Country')
async def create(payload:schemas.CreateCountry, db:Session=Depends(get_db)):
    return await crud.country.create(payload, db)

@router.get('/countries', description='', response_model=schemas.CountryList, name='Countries')
@ContentQueryChecker(crud.country.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.country.read(params, db)

@router.get('/countries/{resource_id}', description='', response_model=schemas.Country, name='Country')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.country.read_by_id(resource_id, db)

@router.patch('/countries/{resource_id}', description='', response_model=schemas.Country, name='Country')
async def update(resource_id:int, payload:schemas.UpdateCountry, db:Session=Depends(get_db)):
    return await crud.country.update(resource_id, payload, db)

@router.delete('/countries/{resource_id}', description='', name='Country')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.country.delete(resource_id, db)

@router.post('/sub-countries', description='', response_model=schemas.SubCountry, status_code=201, name='Sub Country')
async def create(payload:schemas.CreateSubCountry, db:Session=Depends(get_db)):
    return await crud.sub_country.create(payload, db)

@router.get('/sub-countries', description='', response_model=schemas.SubCountryList, name='Sub Countries')
@ContentQueryChecker(crud.sub_country.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.sub_country.read(params, db)

@router.get('/sub-countries/{resource_id}', description='', response_model=schemas.SubCountry, name='Sub Country')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.sub_country.read_by_id(resource_id, db)

@router.patch('/sub-countries/{resource_id}', description='', response_model=schemas.SubCountry, name='Sub Country')
async def update(resource_id:int, payload:schemas.UpdateCountry, db:Session=Depends(get_db)):
    return await crud.sub_country.update(resource_id, payload, db)

@router.delete('/sub-countries/{resource_id}', description='', name='Sub Country')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.sub_country.delete(resource_id, db)

@router.post('/cities', description='', response_model=schemas.City, status_code=201, name='City')
async def create(payload:schemas.CreateCity, db:Session=Depends(get_db)):
    return await crud.city.create(payload, db)

@router.get('/cities', description='', response_model=schemas.CityList, name='Cities')
@ContentQueryChecker(crud.city.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.city.read(params, db)

@router.get('/cities/{resource_id}', description='', response_model=schemas.City, name='City')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.city.read_by_id(resource_id, db)

@router.patch('/cities/{resource_id}', description='', response_model=schemas.City, name='City')
async def update(resource_id:int, payload:schemas.UpdateCity, db:Session=Depends(get_db)):
    return await crud.city.update(resource_id, payload, db)

@router.delete('/cities/{resource_id}', description='', name='City')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.city.delete(resource_id, db)