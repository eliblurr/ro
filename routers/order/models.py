from sqlalchemy import Column, String, Integer, Enum, select, func, and_, ForeignKey
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property
from mixins import BaseMixin, BaseMethodMixin
from routers.voucher.models import Voucher
from routers.meal.models import Meal
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

# countable & non countable

class OrderMeal(BaseMethodMixin, Base):
    '''Order Meal Association Model'''
    __tablename__ = "order_meals"

    meal = relationship('Meal')
    quantity = Column(Integer, nullable=False) # -> translates to number of occrences
    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    status = Column(Enum(OrderMealState), default=OrderMealState.pending, nullable=False) 
    sub_total = column_property((select(Meal.cost).where(Meal.id==meal_id).correlate_except(Meal).scalar_subquery()) * quantity)
    
class Order(BaseMixin, Base):
    '''Order Model'''
    __tablename__ = "orders"

    meals = relationship('OrderMeal', uselist=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    voucher = relationship('Voucher', back_populates="order")
    order_code = Column(String, nullable=False, default=gen_code)
    restaurant = relationship("Restaurant", back_populates="orders")
    voucher_id = Column(Integer, ForeignKey('vouchers.id'), unique=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), unique=True) 
    status = Column(Enum(OrderState), default=OrderState.active, nullable=False) 
    served_total = column_property(
        select(func.sum(OrderMeal.sub_total)).
        where(and_(OrderMeal.status==OrderMealState.served, OrderMeal.order_id==1)).
        correlate_except(OrderMeal).scalar_subquery()
    )

    @hybrid_property
    def total(self):
        total = self.served_total if self.served_total is not None else 0
        if self.voucher:
            return total - (self.voucher.discount*total)
        return total
    
    @hybrid_property
    def currency(self):
        return self.restaurant.city.subcountry.country.currency.title
    
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

