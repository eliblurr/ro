from sqlalchemy import Column, String
from utils import to_tsvector_ix
from mixins import BaseMixin
from database import Base

class Meal(BaseMixin, Base):
    '''Meal Model'''
    __tablename__ = "meals"

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    # images = relationship('ItemImage', backref="restaurant", uselist=True, cascade="all, delete")

class MealImage():
    pass