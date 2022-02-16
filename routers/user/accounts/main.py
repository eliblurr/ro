from fastapi import APIRouter, Depends, HTTPException
from utils import http_exception_detail
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas
from typing import Union

router = APIRouter()

def verify_payload(accounttype:schemas.AccountTypes, payload:Union[schemas.CreateAdmin, schemas.CreateUser,  schemas.CreateCustomer]):
    case1 = accounttype.value=='customers' and payload.__class__==schemas.CreateCustomer
    case2 = accounttype.value=='admins' and payload.__class__==schemas.CreateAdmin
    case3 = accounttype.value=='users' and payload.__class__==schemas.CreateUser
    if not any((case1, case2, case3)):
        raise HTTPException(status_code=422, detail=http_exception_detail([accounttype, payload.dict()], msg='payload mismatch with account type', type="Payload_AccountType mismatch"))
    return {'payload':payload, 'accounttype':accounttype.value}

@router.post('/{usertype}/', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], status_code=201, name='Accounts')
async def create(data=Depends(verify_payload), db:Session=Depends(get_db)):
    if data['accounttype']=='users':
        return await crud.users.create(data['payload'], db)
    if data['accounttype']=='admins':
        return await crud.admins.create(data['payload'], db)
    if data['accounttype']=='customers':
        return await crud.customers.create(data['payload'], db)

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

@router.get('/{accounttype}/{resource_id}', description='', response_model=Union[schemas.Customer, schemas.User, schemas.Admin], name='All Accounts')
async def read_by_id(accounttype:schemas.AccountTypes, resource_id:int, db:Session=Depends(get_db)):
    if accounttype.value == 'users':
        return await crud.users.read_by_id(resource_id, db)
    if accounttype.value == 'admins':
        return await crud.admins.read_by_id(resource_id, db)
    if accounttype.value == 'customers':
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

@router.delete('/{accounttype}/{resource_id}', description='', name='All Accounts')
async def delete(accounttype:schemas.AccountTypes, resource_id:int, db:Session=Depends(get_db)):
    if accounttype.value == 'users':
        return await crud.users.delete(resource_id, db)
    if accounttype.value == 'admins':
        return await crud.admins.delete(resource_id, db)
    if accounttype.value == 'customers':
        return await crud.customers.delete(resource_id, db)
