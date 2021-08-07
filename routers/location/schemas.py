from pydantic import BaseModel
from enum import Enum

class ResourceModel(str, Enum):
    city = 'cities'
    country = 'countries'
    subcountry = 'sub-countries'

class Country(BaseModel):
    title: str