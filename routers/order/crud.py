from exceptions import NotFoundError, UnacceptableError
from routers.voucher.models import Voucher
from routers.meal.crud import get_total
from utils import schema_to_model
from . import models, schemas
from cls import CRUD

order = CRUD(models.Order)
order_meal = CRUD(models.OrderMeal)

def parse_order_meals(order_meals):
    return [schemas.OrderMealBase(meal_id=meal.meal_id) for meal in order_meals for i in range(meal.quantity)]

def verify_voucher(voucher_id, total, db):
    voucher = db.query(Voucher).get(voucher_id)
    if not voucher:
        raise NotFoundError('Voucher not found')

    if not voucher.is_qualified(total):
        raise UnacceptableError('cannot use this voucher for order total')

def verify_order(order_meals, voucher_id, db):
    if voucher_id:
        total = get_total([(m.meal_id, m.quantity) for m in order_meals], db)
        return verify_voucher(voucher_id, total, db)
    return parse_order_meals(order_meals)

# meals = crud.verify_order(payload.meals, payload.voucher_id, db)
# if meals:
#     await crud.update_or_create_meal(meals, db)
# async def update_or_create_meal(meals, db):
#     for meal in meals:
#         obj = db.query(models.Meal).get(meal.meal_id)
#         if obj:
#             [setattr(obj, k, v) for k, v in meal.__dict__.items()]
#         else: 
#             obj = models.Meal(**schema_to_model(meal))
#             db.add(obj)
# async def update_order(order_id, payload, db):
#     order = db.query(models.Order).get(order_id)
#     if not order:
#         raise NotFoundError('Order not found')
#     if payload.meals:
#         meal_id_quan = [(m.id, m.quantity) for m in order.meals]
#     # if payload.voucher_id:
#     #     verify_voucher(voucher_id, total, db)
#     [setattr(obj, k, v) for k, v in payload.copy(exclude={'meals'}).__dict__.items()]


