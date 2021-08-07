from fastapi import APIRouter, Depends
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List, Union
from . import crud, schemas

router = APIRouter()

@router.get("/class-decor-param/")
@ContentQueryChecker(crud.sub_country.model.c(), 'kl')
def test(a:int=None, n:int=None, db:Session=Depends(get_db), **query_params):
    print(query_params, db)

'''
    # split q @ :
    # get index[0] @ sort
    # verify datatypes for params in request
    # optional control query
    # exact cols val

    # **{self.alias+'__pk__exact':id}
    # **{key+'something':Depends()}

    # params[:-1]

    class ResourceResolve:
        def __init__(self, model:schemas.ResourceModel, payload:Union[schemas.Country,]):
            self.model = model
            self.payload = payload

        def model(self):
            return self.model

        def payload(self):
            return self.payload

    async def model(model:schemas.Model):
        return crud.country if model is schemas.Model.country \
        else crud.subcountry if model is schemas.Model.country \
        else crud.city

    async def pair(payload:Union[schemas.Country,], model=Depends(model)):
        if model and payload:
            return model, payload,
        return model

    @router.get('/{model}', description='')
    async def read(model=Depends(model), search:str=None, value:str=None, skip:int=0, limit:int=100, db:Session=Depends(get_db)):
        return await model.read(db, search, value, skip, limit)

    @router.get('/{model}/{id}', description='')
    async def read_by_id(id:int, model=Depends(model), db:Session=Depends(get_db)):
        return await model.read_by_id(id, db)

    @router.patch('/{model}/{id}', description='')
    async def update(id:int, pair:dict=Depends(pair), db:Session=Depends(get_db)):
        return await pair[0].update(id, pair[1], db)

    @router.delete('/{model}/{id}', description='')
    async def delete(id:int, model=Depends(model), db:Session=Depends(get_db)):
        return await model.delete(id, db)

'''