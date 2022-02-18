from . import models, schemas
from typing import List
from cls import CRUD

menu = CRUD(models.Menu)
menu_meal = CRUD(models.MenuMeal)

async def add_meal_to_menu(menu_id: int, meal_ids: List[int], db):
    payload = [schemas.MenuMeal(menu_id=menu_id, meal_id=id) for id in meal_ids]
    return await menu_meal.bk_create(payload, db)

async def rem_meal_from_menu(menu_id: int, meal_ids: List[int], db):
    return await menu_meal.bk_delete(meal_ids, db, use_field='meal_id', menu_id=menu_id)