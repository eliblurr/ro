from . import models, schemas
from sqlalchemy import func
from cls import CRUD

meal = CRUD(models.Meal)

def get_total(meal_id_quan, db):
    return sum(
        list(
            filter(
                None,
                [
                    db.query(
                        func.sum(models.Meal.cost)*item[1]
                    ).filter(models.Meal.id==item[0]).scalar() for item in meal_id_quan
                ]
            )
        )
    )