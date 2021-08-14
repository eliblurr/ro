from . import models, schemas
from cls import CRUD

meal = CRUD(models.Meal)
meal_image = CRUD(models.MealImage)