from sqlalchemy.orm import Session
from . import models, schemas
from cls import CRUD

role = CRUD(models.Role)

# custom update