from fastapi import APIRouter, Depends, HTTPException
from utils import http_exception_detail
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import Union

router = APIRouter()

def verify_create(usertype:schemas.UserTypes, payload:Union[schemas.CreateCustomer, schemas.CreateUser, schemas.CreateAdmin]):
    case1 = usertype.value == 'customers' and payload.__class__==schemas.CreateCustomer
    case2, case3 = usertype.value == 'admins' and payload.__class__==schemas.CreateAdmin, usertype.value == 'users' and payload.__class__==schemas.CreateUser
    if not (case1 or case2 or case3):
        raise HTTPException(status_code=422, detail=http_exception_detail([usertype, payload.dict()], msg='selected userType mismatch with payload', type="Payload_UserType mismatch"))
    return {'payload':payload, 'usertype':usertype.value}

def verify_update(usertype:schemas.UserTypes, payload:Union[schemas.UpdateCustomer, schemas.UpdateUser, schemas.UpdateAdmin]):
    case1 = usertype.value == 'customers' and payload.__class__==schemas.UpdateCustomer
    case2, case3  = usertype.value == 'admins' and payload.__class__==schemas.UpdateAdmin, usertype.value == 'users' and payload.__class__==schemas.UpdateUser
    if not (case1 or case2 or case3):
        raise HTTPException(status_code=422, detail=http_exception_detail([usertype, payload.dict()], msg='selected userType mismatch with payload', type="Payload_UserType mismatch"))
    return {'payload':payload, 'usertype':usertype.value}
   
@router.post('/{usertype}/', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], status_code=201, name='Accounts')
async def create(data=Depends(verify_create), db:Session=Depends(get_db)):
    if data['usertype'] == 'users':
        return await crud.users.create(data['payload'], db)
    if data['usertype'] == 'admins':
        return await crud.admins.create(data['payload'], db)
    if data['usertype'] == 'customers':
        return await crud.customers.create(data['payload'], db)

@router.get('/users/', description='', response_model=schemas.UserList, name='Accounts[User]')
@ContentQueryChecker(crud.users.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.users.read(params, db)

@router.get('/admins/', description='', response_model=schemas.AdminList, name='Accounts[Admin]')
@ContentQueryChecker(crud.admins.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.admins.read(params, db)

@router.get('/customers/', description='', response_model=schemas.CustomerList, name='Accounts[Customer]')
@ContentQueryChecker(crud.customers.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.customers.read(params, db)

@router.get('/{usertype}/{resource_id}', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], name='Accounts')
async def read_by_id(usertype:schemas.UserTypes, resource_id:int, db:Session=Depends(get_db)):
    if usertype.value == 'users':
        return await crud.users.read_by_id(resource_id, db)
    if usertype.value == 'admins':
        return await crud.admins.read_by_id(resource_id, db)
    if usertype.value == 'customers':
        return await crud.customers.read_by_id(resource_id, db)

@router.patch('/{usertype}/{resource_id}', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], name='Accounts')
async def update(data=Depends(verify_update), db:Session=Depends(get_db)):
    if data['usertype'] == 'users':
        return await crud.users.update(resource_id, data['payload'], db)
    if data['usertype'] == 'admins':
        return await crud.admins.update(resource_id, data['payload'], db)
    if data['usertype'] == 'customers':
        return await crud.customers.update(resource_id, data['payload'], db)

@router.delete('/{usertype}/{resource_id}', description='', name='Accounts')
async def delete(usertype:schemas.UserTypes, resource_id:int, db:Session=Depends(get_db)):
    if usertype.value == 'users':
        return await crud.users.delete(resource_id, db)
    if usertype.value == 'admins':
        return await crud.admins.delete(resource_id, db)
    if usertype.value == 'customers':
        return await crud.customers.delete(resource_id, db)