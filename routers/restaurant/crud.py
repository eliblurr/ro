from . import models, schemas
from cls import CRUD

restaurant = CRUD(models.Restaurant)

from exceptions import NotFoundError

async def get_uploads(resource_id:int, upload:schemas.Uploads, offset:int, limit:int, db):
    res = await restaurant.read_by_id(resource_id, db)
    if not res:
        raise NotFoundError(f"restaurant with id:{resource_id} not found")

    if upload.value=="images":return res.images[offset:offset+limit]
    elif upload.value=="documents":return res.documents[offset:offset+limit]
    elif upload.value=="audio":return res.audio[offset:offset+limit]
    elif upload.value=="videos":return res.videos[offset:offset+limit]