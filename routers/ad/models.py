from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from routers.media.models import Image
from utils import to_tsvector_ix
from mixins import BaseMixin
from database import Base

class AD(BaseMixin, Base):
    '''AD Model'''
    __tablename__ = "ads"

    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    images = relationship('Image', uselist=True, cascade="all, delete")