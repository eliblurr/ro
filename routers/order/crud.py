from . import models, schemas
from cls import CRUD

order = CRUD(models.Order)
order_meal = CRUD(models.OrderMeal)