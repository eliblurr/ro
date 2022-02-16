from . import models, schemas
from typing import List
from cls import CRUD

category = CRUD(models.Category)

schema = {
    schemas.RelatedResource.meals: (CRUD(models.CategoryMeal), schemas.CategoryMeal, 'meal_id'),
    schemas.RelatedResource.menus: (CRUD(models.CategoryMenu), schemas.CategoryMenu, 'menu_id')
}

async def add_resource_to_category(cat_id: int, resource_ids: List[int], child:schemas.RelatedResource, db):
    obj = schema.get(child)
    payload = [obj[1](category_id=cat_id, c_id=id)for id in resource_ids]
    return await obj[0].bk_create(payload, db)

async def rem_resource_from_category(cat_id: int, resource_ids: List[int], child:schemas.RelatedResource, db):
    obj = schema.get(child)
    return await obj[0].bk_delete(resource_ids, db, use_field=obj[2], category_id=cat_id)