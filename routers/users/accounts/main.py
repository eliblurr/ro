from fastapi import APIRouter, Depends, HTTPException
from utils import http_exception_detail
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import Union

router = APIRouter()

@router.post('/users', description='Create Restaurant User Account', response_model=schemas.User, status_code=201, name='Restaurant User/Staff Accounts')
async def create(payload:schemas.CreateUser, db:Session=Depends(get_db)):
    return await crud.users.create(payload, db)

@router.post('/admins', description='Create System Administrator Account', response_model=schemas.Admin, status_code=201, name='System Administrator Accounts')
async def create(payload:schemas.CreateAdmin, db:Session=Depends(get_db)):
    return await crud.admins.create(payload, db)
    
@router.post('/customers', description='Create Customer Account', response_model=schemas.Customer, status_code=201, name='Customer Accounts')
async def create(payload:schemas.CreateCustomer, db:Session=Depends(get_db)):
    return await crud.customers.create(payload, db)

@router.get('/users', description='', response_model=schemas.UserList, name='Restaurant User/Staff Accounts')
@ContentQueryChecker(crud.users.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.users.read(params, db)

@router.get('/admins', description='', response_model=schemas.AdminList, name='System Administrator Accounts')
@ContentQueryChecker(crud.admins.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.admins.read(params, db)

@router.get('/customers', description='', response_model=schemas.CustomerList, name='Customer Accounts')
@ContentQueryChecker(crud.customers.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.customers.read(params, db)

@router.get('/{usertype}/{resource_id}', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], name='All Accounts')
async def read_by_id(usertype:schemas.UserTypes, resource_id:int, db:Session=Depends(get_db)):
    if usertype.value == 'users':
        return await crud.users.read_by_id(resource_id, db)
    if usertype.value == 'admins':
        return await crud.admins.read_by_id(resource_id, db)
    if usertype.value == 'customers':
        return await crud.customers.read_by_id(resource_id, db)

@router.patch('/customers/{resource_id}', description='', response_model=schemas.Customer, name='Customer Accounts')
async def update(resource_id:int, payload:schemas.UpdateCustomer, db:Session=Depends(get_db)):
    return await crud.customers.update(resource_id, payload, db)

@router.patch('/users/{resource_id}', description='', response_model=schemas.User, name='Restaurant User/Staff Accounts')
async def update(resource_id:int, payload:schemas.UpdateUser, db:Session=Depends(get_db)):
    if payload.password:
        payload.password = payload.Meta.model.generate_hash(payload.password)
    return await crud.users.update(resource_id, payload, db)

@router.patch('/admins/{resource_id}', description='', response_model=schemas.Admin, name='System Administrator Accounts')
async def update(resource_id:int, payload:schemas.UpdateAdmin, db:Session=Depends(get_db)):
    if payload.password:
        payload.password = payload.Meta.model.generate_hash(payload.password)
    return await crud.admins.update(resource_id, payload, db)

@router.delete('/{usertype}/{resource_id}', description='', name='All Accounts')
async def delete(usertype:schemas.UserTypes, resource_id:int, db:Session=Depends(get_db)):
    if usertype.value == 'users':
        return await crud.users.delete(resource_id, db)
    if usertype.value == 'admins':
        return await crud.admins.delete(resource_id, db)
    if usertype.value == 'customers':
        return await crud.customers.delete(resource_id, db)

# def verify_create(usertype:schemas.UserTypes, payload:Union[schemas.CreateAdmin, schemas.CreateUser,  schemas.CreateCustomer, ]):
#     case1 = usertype.value == 'customers' and payload.__class__==schemas.CreateCustomer
#     case2 = usertype.value == 'admins' and payload.__class__==schemas.CreateAdmin
#     case3 = usertype.value == 'users' and payload.__class__==schemas.CreateUser
#     print(case1, case2, case3)
#     if not any(case1 or case2 or case3):
#         raise HTTPException(status_code=422, detail=http_exception_detail([usertype, payload.dict()], msg='selected userType mismatch with payload', type="Payload_UserType mismatch"))
#     return {'payload':payload, 'usertype':usertype.value}

# @router.post('/{usertype}/', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], status_code=201, name='Accounts')
# async def create(data=Depends(verify_create), db:Session=Depends(get_db)):
#     if data['usertype'] == 'users':
#         return await crud.users.create(data['payload'], db)
#     if data['usertype'] == 'admins':
#         return await crud.admins.create(data['payload'], db)
#     if data['usertype'] == 'customers':
#         return await crud.customers.create(data['payload'], db)