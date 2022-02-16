from fastapi import APIRouter, Depends, File, UploadFile, Body, HTTPException
from sqlalchemy.exc import StatementError
from utils import http_exception_detail
from config import UPLOAD_EXTENSIONS
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import Union, List
from . import crud, schemas
import pathlib

router = APIRouter()

def verify_ext(upload_type:schemas.UploadType, files:List[UploadFile]=File(None)):
    try:
        for file in files:
            assert pathlib.Path(file.filename).suffix in UPLOAD_EXTENSIONS[upload_type.value.upper()], f"unsupported format for {upload_type.value.upper()}"
        return upload_type, files
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=http_exception_detail(msg=f"{e}", type=e.__class__.__name__))

@router.post('/{object}/{object_id}/{upload_type}', description='', status_code=201, name='Upload')
async def create(object:crud.Object, object_id:int, files=Depends(verify_ext), db:Session=Depends(get_db)):
    try:
        obj = crud.objects[object.value]
        return await crud.create(files[1], obj, object_id, files[0], db)
    except StatementError as e:
        raise HTTPException(status_code=400, detail=http_exception_detail(msg=e._message(), type=e.__class__.__name__))
    except crud.NotFoundError as e:
        raise HTTPException(status_code=404, detail=http_exception_detail(msg=e._message(), type=e.__class__.__name__))
    except Exception as e:
        raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message(), type=e.__class__.__name__))

@router.delete('/{resource_id}', description='', name='Upload')
async def delete(resource_id:int, db:Session=Depends(get_db)):
    return await crud.delete(resource_id, db)