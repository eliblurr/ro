from . import models
from cls import CRUD

city = CRUD(models.City)
country = CRUD(models.Country)
sub_country = CRUD(models.SubCountry)