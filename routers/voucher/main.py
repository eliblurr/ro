from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from . import crud, schemas

router = APIRouter()

@router.post('/', description='', response_model=schemas.Voucher, status_code=201, name='Voucher')
async def create(payload:schemas.CreateVoucher, db:Session=Depends(get_db)):
    voucher = await crud.voucher.create(payload, db)
    if voucher.expiry:
        crud.schedule_expiry(voucher.id, voucher.expiry)
    return voucher

@router.get('/', description='', response_model=schemas.VoucherList, name='Voucher')
@ContentQueryChecker(crud.voucher.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.voucher.read(params, db)

@router.get('/{resource_id}', description='', response_model=schemas.Voucher, name='Voucher')
async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
    return await crud.voucher.read_by_id(resource_id, db)

@router.patch('/{resource_id}', description='', response_model=schemas.Voucher, name='Voucher')
async def update(resource_id:int, payload:schemas.UpdateVoucher, db:Session=Depends(get_db)):
    voucher = await crud.voucher.update(resource_id, payload, db)
    if voucher.expiry:
        crud.schedule_expiry(voucher.id, voucher.expiry)
    return voucher

@router.delete('/{resource_id}', description='', name='Voucher')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.voucher.delete(resource_id, db)
