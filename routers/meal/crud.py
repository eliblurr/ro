from . import models, schemas
from cls import CRUD

meal = CRUD(models.Meal)

async def add_images(id:int, images, db):
    pass

async def delete_image():
    pass