from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from utils import today_str
from database import Base
from ctypes import File

class AD(BaseMixin, Base):
    '''AD Model'''
    __tablename__ = "ads"
    __table_args__ = (
        CheckConstraint("""COALESCE(title, metatitle, description, image) IS NOT NULL""", name="ck_at_least_one_required"),
    )

    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(File(upload_to=f'{today_str()}'), nullable=True)
    locales = relationship('Locale', secondary='ad_locales', back_populates="ads", lazy='dynamic')
    

class ADLocale(Base):
    '''AD Locale Model[what locales should add be available in]'''
    __tablename__ = 'ad_locales'

    ad_id = Column(Integer, ForeignKey('ads.id'), primary_key=True)
    locale_id = Column(Integer, ForeignKey('locales.id'), primary_key=True)
