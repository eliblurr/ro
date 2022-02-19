# from routers.media.schemas import Image
from pydantic import BaseModel, constr
from routers.meal.schemas import Meal
from routers.menu.schemas import Menu
from constants import PHONE, EMAIL
from typing import Optional, List
from utils import as_form
import datetime, enum

class RestaurantBase(BaseModel):
    title: str
    description: str
    status: Optional[bool]
    metatitle: Optional[str]
    email: constr(regex=EMAIL)
    phone: constr(regex=PHONE)
    postal_address: Optional[str]
    street_address: Optional[str]
    digital_address: Optional[str]

@as_form
class CreateRestaurant(RestaurantBase):
    city_id: int

@as_form
class UpdateRestaurant(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    city_id: Optional[int]
    metatitle: Optional[str]
    description: Optional[str]
    postal_address: Optional[str]
    street_address: Optional[str]
    digital_address: Optional[str]
    email: Optional[constr(regex=EMAIL)]
    phone: Optional[constr(regex=PHONE)]

class Restaurant(RestaurantBase):
    id: int
    logo: str
    created: datetime.datetime
    updated: datetime.datetime
    meals: Optional[List[Meal]]
    
    class Config:
        orm_mode = True

class RestaurantList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Restaurant]

class Uploads(str, enum.Enum):
    audio='audio'
    videos='videos'
    images='images'
    documents='documents'
