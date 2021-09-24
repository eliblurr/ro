from utils import http_exception_detail
from routers.meal.crud  import meal
from fastapi import HTTPException
from . import models, schemas
from cls import CRUD

menu = CRUD(models.Menu)

async def add_meal_to_menu(resource_id, meal_ids, db):
    mn = await menu.read_by_id(resource_id, db)
    if not mn:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc='resource_id', msg=f'menu with id {resource_id} not found', type='NonExist'))
    msg = []
    try:
        for id in meal_ids:
            ml = await meal.read_by_id(id, db)
            if ml and (ml not in mn.meals):
                mn.meals.append(ml)
            else:
                msg.append(id)
        db.commit()
        return "success", {"loc":msg, "info":f"failed" if msg else "all meals added", "msg":"meal(s) already part of menu or no longer exists"}
    except Exception as s:
        raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))

async def remove_meal_from_menu(resource_id, meal_ids, db):
    mn = await menu.read_by_id(resource_id, db)
    if not mn:
        raise HTTPException(status_code=404, detail=http_exception_detail(loc='resource_id', msg=f'menu with id {resource_id} not found', type='NonExist'))
    msg = []
    try:
        for id in meal_ids:
            ml = await meal.read_by_id(id, db)
            if ml and (ml in mn.meals):
                mn.meals.remove(ml)
            else:
                msg.append(id)
        db.commit()
        return "success", {"loc":msg, "info":f"failed" if msg else "all meals removed", "msg":"meal(s) is not part of menu or no longer exists"}
    except Exception as s:
        raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))