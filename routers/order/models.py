from sqlalchemy import Column, String, Integer, Enum, select, func, and_, ForeignKey
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


class OrderMeal(Base):
    '''Order Meal Association Model'''
    __tablename__ = "order_meals"

    sub_total = 90
    meal = relationship('Meal')
    quantity = Column(Integer, nullable=False)
    # sub_total = column_property(meal.cost*quantity)
    meal_id = Column(Integer, ForeignKey('meals.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    status = Column(Enum(OrderMealState), default=OrderMealState.pending, nullable=False) 
    
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
    total_to_pay = 90
    # total_to_pay = column_property(total-voucher.discount(total))
    
    # payment
    # paymentMethod
    # paymentMethodId
    # bill
    # discountCode
    # currency primary join relationship
    # discount
    # trigger if paid change status to completed
    # make payments to close session

