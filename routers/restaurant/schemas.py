from routers.media.schemas import Image
from routers.meal.schemas import Meal
from routers.menu.schemas import Menu
from typing import Optional, List
from pydantic import BaseModel
from utils import as_form
import datetime

# title = Column(String, nullable=False)
# metatitle = Column(String, nullable=True)
# description = Column(String, nullable=False)
# meals = relationship('Meal', uselist=True, cascade="all, delete")
# images = relationship('Image', uselist=True, cascade="all, delete")
# menus = relationship('Menu', secondary='restaurant_menus', backref=backref('restaurant'), lazy='dynamic')

class RestaurantBase(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]

@as_form
class CreateRestaurant(RestaurantBase):
    city_id: int

class UpdateRestaurant(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
    restaurant_id: Optional[int]

class Restaurant(RestaurantBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime
    meals: Optional[List[Meal]]
    images: Optional[List[Image]]

    class Config:
        orm_mode = True

class RestaurantList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Restaurant]