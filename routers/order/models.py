from sqlalchemy import Column, String, Integer, Enum, select, and_, ForeignKey, Float
from sqlalchemy.orm import relationship, column_property, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import IntegrityError
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
    completed = 'completed' # meaning paid
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
    meal_id = Column(Integer, ForeignKey('meals.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Enum(OrderMealState), default=OrderMealState.pending, nullable=False) 
    sub_total = column_property((select(Meal.cost).where(Meal.id==meal_id).correlate_except(Meal).scalar_subquery()))

    # quantity = Column(Integer, nullable=False) # -> translates to number of occurrence
    # sub_total = column_property((select(Meal.cost).where(Meal.id==meal_id).correlate_except(Meal).scalar_subquery()) * quantity)

    # @validates('quantity')
    # def validate_phone(self, key, value):
    #     assert value > 0, 'Quantity must be at least 1'
    #     return value

def restaurant_id(context):
    id = context.connection.execute(select(Table.restaurant_id).where(Table.__table__.c.id==context.get_current_parameters()["table_id"])).scalar()
    if not id:
        raise IntegrityError('no restaurant_id available for table_id', 'table_id', 'could not resolve restaurant_id from table')
    return id

class Order(BaseMixin, Base):
    '''Order Model'''
    __tablename__ = "orders"

    amount_paid = Column(Float)
    meals = relationship('OrderMeal', uselist=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    table = relationship("Table", back_populates="orders")
    voucher_id = Column(Integer, ForeignKey('vouchers.id'))
    voucher = relationship('Voucher', back_populates="order")
    order_code = Column(String, nullable=False, unique=True, default=gen_code)
    restaurant = relationship("Restaurant", back_populates="orders")
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Enum(OrderState), default=OrderState.active, nullable=False) 
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), default=restaurant_id) 
    served_total = column_property(
        select(
            func.sum(OrderMeal.sub_total)
        ).where(
            OrderMeal.status==OrderMealState.served, 
            OrderMeal.order_id==id
        ).correlate_except(OrderMeal).scalar_subquery())

    def total(self):
        total = self.served_total if self.served_total is not None else 0
        if self.voucher:
            return total - self.voucher.discount
        return total

    def currency(self):
        return self.restaurant.locale.get_currency()

    def currency_symbol(self):
        return self.restaurant.locale.get_currency_symbol()

    def formatted_total(self):
        total = self.total()
        return self.restaurant.locale.format_currency(total)

    def set_payment(self, amount):
        total = self.total()
        if amount==total:
            self.status = 'completed'
            self.amount_paid = total