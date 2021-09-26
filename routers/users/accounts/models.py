from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger, sql
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from mixins import BaseMixin, HashMethodMixin
from routers.users.role.models import Role
from constants import PHONE, EMAIL
from utils import gen_code
from database import Base
import re

class User(BaseMixin, HashMethodMixin, Base):
    '''User Model'''
    __tablename__ = "users"
    
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', back_populates="users")
    permissions = Column(BigInteger, nullable=False, default=0)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship('Restaurant', back_populates="users")
    code = Column(String, nullable=False, default=gen_code, unique=True)

    @validates('password', include_removes=True)
    def validate_password(self, key, password, is_remove):
        assert len(password) > 5, 'unacceptable password length'
        return self.__class__.generate_hash(password)

class Admin(BaseMixin, HashMethodMixin, Base):
    '''Admin Model'''
    __tablename__ = "admins"

    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    permissions = Column(BigInteger, nullable=False, default=0)
    
    @validates('email')
    def validate_email(self, key, value):
        assert re.search(EMAIL, value), 'invalid email format'
        return value

    @validates('password', include_removes=True)
    def validate_password(self, key, password, is_remove):
        assert len(password) > 5, 'unacceptable password length'
        return self.__class__.generate_hash(password)

class Customer(BaseMixin, Base):
    '''Customer Model'''
    __tablename__ = "customers"

    last_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    phone = Column(String, nullable=False, unique=True)
    permissions = Column(BigInteger, nullable=False, default=0)
    
    @validates('phone')
    def validate_phone(self, key, value):
        assert re.search(PHONE, value), 'invalid phone format'
        return value

    @hybrid_property
    def full_name(self):
        return f"{self.first_name+' ' if self.first_name  else ''}{self.middle_name+' ' if self.middle_name  else ''}{self.last_name+' ' if self.last_name  else ''}"