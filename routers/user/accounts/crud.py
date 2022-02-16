from . import models, schemas
from cls import CRUD

users = CRUD(models.User)
admins = CRUD(models.Admin)
customers = CRUD(models.Customer)