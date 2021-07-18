from . import models
from cls import CRUD

city = CRUD(models.City)
country = CRUD(models.Country)
subCountry = CRUD(models.SubCountry)