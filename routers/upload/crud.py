from utils import http_exception_detail
from exceptions import NotFoundError
from fastapi import HTTPException
from enum import Enum
from . import models

from routers.restaurant.models import Restaurant

objects = {
    'restaurants': Restaurant
}

Object = Enum('Object', {
    v:v for v in objects.keys()
})

async def create(files, object, object_id, upload_type, db):
    obj = db.query(object).get(object_id)
    if obj is None:
        raise NotFoundError(f"object with id:{object_id} not found")
    db.add_all([
        models.Upload(
            url=f,
            upload_type=upload_type,
            object = obj
        )
        for f in files
    ])
    db.commit()
    return "upload successful"
 
async def delete(id, db):
    obj = models.Upload.query.filter_by(id=id).one()
    db.delete(obj)
    return True