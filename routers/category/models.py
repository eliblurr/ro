from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from utils import async_remove_file
from mixins import BaseMixin
from utils import today_str
from database import Base
from ctypes import File

class Category(BaseMixin, Base):
    '''Category Model'''
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint('title', 'restaurant_id', name='uix_cat_title_restaurant_fk'),)
    
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=True)
    image = Column(File(upload_to=f'{today_str()}'), nullable=False)
    meals = relationship('Meal', secondary='category_meals', backref='categories', lazy='dynamic')
    menus = relationship('Menu', secondary='category_menus', backref='categories', lazy='dynamic')

class CategoryMeal(Base):
    '''Category Meal Model'''
    __tablename__ = 'category_meals'

    meal_id = Column(Integer, ForeignKey('meals.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)

class CategoryMenu(Base):
    '''Category Menu Model'''
    __tablename__ = 'category_menus'

    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)

@event.listens_for(Category, 'after_delete')
def receive_after_delete(mapper, connection, target):
    if target.image:async_remove_file(target.image)

@event.listens_for(Category.image, 'set', propagate=True)
def receive_set(target, value, oldvalue, initiator):
    if oldvalue:async_remove_file(oldvalue)

@event.listens_for(Category, 'before_insert')
def verify_target_title(mapper, connection, target):
    res = connection.execute(Category.__table__.select().where(Category.__table__.c.restaurant_id==None, Category.__table__.c.title==target.title))
    if res.rowcount:  
        raise IntegrityError(f"custom select @@ restaurant_id is NULL AND title={target.title}", 'title', f'DETAIL:  Key (title)=({target.title}) already exists.\n')  