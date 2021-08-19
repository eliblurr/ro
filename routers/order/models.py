from sqlalchemy import Column, String, Integer, Enum, select, func, and_
from sqlalchemy.orm import relationship, column_property
from routers.voucher.models import Voucher
from routers.meal.models import Meal
from mixins import BaseMixin
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
    cancelled = 'cancelled'
    
class Order(BaseMixin, Base):
    '''Order Model'''
    __tablename__ = "orders"

    meals = relationship('OrderMeal', uselist=True)
    voucher = relationship('Voucher', uselist=False)
    table_id = Column(Integer, ForeignKey('tables.id'))
    order_code = Column(String, nullable=False, default=gen_code)
    status = Column(Enum(OrderState), default=OrderState.active, nullable=False) 
    total = column_property(
        select(func.sum(OrderMeal.sub_total)).
        where(and_(
            OrderMeal.status==OrderMealState.served, OrderMeal.order_id==id
        )).correlate_except(OrderMeal).scalar_subquery()
    )
    # voucher_id = Column(Integer, ForeignKey('vouchers.id'))
    
    
    # amount_to_pay = column_property(total-voucher.discount)
    # payment
    # paymentMethod
    # paymentMethodId
    
    # bill
    # discountCode
    # discount
    # trigger if paid change status to completed
    # make payments to close session

class OrderMeal(Base):
    '''Order Meal Association Model'''
    __tablename__ = "order_meals"

    meal = relationship('Meal')
    quantity = Column(Integer, nullable=False)
    sub_total = column_property(meal.cost*quantity)
    order_id = Column(Integer, ForeignKey('orders.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'), nullable=False)
    status = Column(Enum(OrderMealState), default=OrderMealState.pending, nullable=False) 
