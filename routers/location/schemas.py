from pydantic import BaseModel
from config import locale
import enum

LocaleChoice = enum.Enum('LocaleChoice', locale.territories)

class AddLocale(BaseModel):
    name: str

class RelatedResource(enum.Enum):
    ads='ads'
    restaurants='restaurants'