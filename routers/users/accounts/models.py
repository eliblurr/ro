from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from routers.users.role.models import Role
from constants import PHONE, EMAIL
from mixins import BaseMixin
from database import Base

class User(BaseMixin, Base):
    '''User Model'''
    __tablename__ = "users"

    code = Column(String, nullable=False)
    password = Column(String, nullable=False)
    roles = relationship('Role', back_populates="users")
    role_id = Column(Integer, ForeignKey('roles.id'))
    restaurant = relationship('Restaurant', back_populates="users")
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    permission = 0
    
class Admin(BaseMixin, Base):
    '''Admin Model'''
    __tablename__ = "admins"

    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    permission = 0
    
    @validates('email')
    def validate_email(self, key, value):
        assert re.search(EMAIL, value), 'invalid email format'
        return value

class Customer(BaseMixin, Base):
    '''Customer Model'''
    __tablename__ = "customers"

    phone = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    permissions = 0
    
    @validates('phone')
    def validate_phone(self, key, value):
        assert re.search(PHONE, value), 'invalid phone format'
        return value

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"