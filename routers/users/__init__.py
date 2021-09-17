# from fastapi import APIRouter, Depends
# from cls import ContentQueryChecker
# from sqlalchemy.orm import Session
# from dependencies import get_db
# from . import crud, schemas

# router = APIRouter()

# @router.post('/', description='', response_model=schemas.FAQ, status_code=201, name='FAQ')
# async def create(payload:schemas.CreateFAQ, db:Session=Depends(get_db)):
#     return await crud.faq.create(payload, db)

# @router.get('/', description='', response_model=schemas.FAQList, name='FAQ')
# @ContentQueryChecker(crud.faq.model.c(), None)
# async def read(db:Session=Depends(get_db), **params):
#     return await crud.faq.read(params, db)

# @router.get('/{resource_id}', description='', response_model=schemas.FAQ, name='FAQ')
# async def read_by_id(resource_id:int, db:Session=Depends(get_db)):
#     return await crud.faq.read_by_id(resource_id, db)

# @router.patch('/{resource_id}', description='', response_model=schemas.FAQ, name='FAQ')
# async def update(resource_id:int, payload:schemas.UpdateFAQ, db:Session=Depends(get_db)):
#     return await crud.faq.update(resource_id, payload, db)

# @router.delete('/{resource_id}', description='', name='FAQ')
# async def delete(resource_id:int, db:Session=Depends(get_db)):
#     return await crud.faq.delete(resource_id, db)
