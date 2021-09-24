from typing import Optional, List
from pydantic import BaseModel
from enum import Enum
import datetime

class Resource(str, Enum):
    city = 'cities'
    country = 'countries'
    subcountry = 'sub-countries'

class CountryBase(BaseModel):
    title: str
    
class CreateCountry(CountryBase):
    currency_id: int

class UpdateCountry(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    currency_id: Optional[int]

class Country(CountryBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class CountryList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Country]
    
class SubCountryBase(BaseModel):
    title: str
    postcode: str

class CreateSubCountry(SubCountryBase):
    country_id: int

class UpdateSubCountry(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    postcode: Optional[str]
    country_id: Optional[int]

class SubCountry(Country):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class SubCountryList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[SubCountry]

class CityBase(BaseModel):
    title: str
    postcode: Optional[str]

class CreateCity(CityBase):
    subcountry_id:int

class UpdateCity(BaseModel):
    title: Optional[str]
    status: Optional[bool]
    postcode: Optional[str]
    subcountry_id: Optional[int]

class City(CityBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class CityList(CityBase):
    bk_size: int
    pg_size: int
    data: List[City]