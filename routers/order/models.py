from sqlalchemy import Column, String, Integer, Enum, select, and_, ForeignKey, Float
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property
from mixins import BaseMixin, BaseMethodMixin
from routers.voucher.models import Voucher
from routers.table.models import Table
from routers.meal.models import Meal
from sqlalchemy.sql import func
from utils import gen_code
from database import Base
import enum

class OrderState(enum.Enum):
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'

class OrderMealState(enum.Enum):
    ready = 'ready'
    served = 'served'
    pending = 'pending'
    preparing = 'preparing'

class OrderMeal(BaseMethodMixin, Base):
    '''Order Meal Association Model'''
    __tablename__ = "order_meals"

    meal = relationship('Meal', uselist=False)
    quantity = Column(Integer, nullable=False) # -> translates to number of occrences
    meal_id = Column(Integer, ForeignKey('meals.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Enum(OrderMealState), default=OrderMealState.pending, nullable=False) 
    sub_total = column_property((select(Meal.cost).where(Meal.id==meal_id).correlate_except(Meal).scalar_subquery()) * quantity)

def restaurant_id(context):
    id = context.connection.execute(select(Table.restaurant_id).where(Table.__table__.c.id==context.get_current_parameters()["table_id"]))
    return id.first()[0]

class Order(BaseMixin, Base):
    '''Order Model'''
    __tablename__ = "orders"

    amount_paid = Column(Float)
    meals = relationship('OrderMeal', uselist=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    table = relationship("Table", back_populates="orders")
    voucher = relationship('Voucher', back_populates="order")
    order_code = Column(String, nullable=False, default=gen_code)
    restaurant = relationship("Restaurant", back_populates="orders")
    voucher_id = Column(Integer, ForeignKey('vouchers.id'), unique=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Enum(OrderState), default=OrderState.active, nullable=False) 
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), default=restaurant_id) 
    served_total = column_property(
        select(
            func.sum(OrderMeal.sub_total
            )
        ).where(
            OrderMeal.status==OrderMealState.served, 
            OrderMeal.order_id==id
        ).correlate_except(OrderMeal).scalar_subquery())
    
    @hybrid_property
    def total(self):
        total = self.served_total if self.served_total is not None else 0
        if self.voucher:
            return total - (self.voucher.discount*total)
        return total

    @hybrid_property
    def currency(self):
        return self.table.restaurant.city.subcountry.country.currency.title

# check constraint on table and status
# if order closed lock
# payment
# paymentMethod
# paymentMethodId
# bill
# discountCode
# currency primary join relationship
# discount
# trigger if paid change status to completed
# make payments to close session
# event to check if there is an active session on table