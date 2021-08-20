from fastapi import APIRouter, Depends, File, UploadFile, Body
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import Union, List
from . import crud, schemas

router = APIRouter()

@router.post('/images', description='', status_code=201, name='Image')
async def create(files:List[UploadFile]=File(None), payload=Depends(schemas.CreateImage.as_form), db:Session=Depends(get_db)):
    return await crud.create(files, payload, db)

@router.delete('/{media}/{resource_id}', description='', name='Media')
async def delete(media:schemas.MediaType, resource_id:int, db:Session=Depends(get_db)):
    return await crud.delete(resource_id, media, db)