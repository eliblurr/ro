from sqlalchemy import Column, String, Integer, event
from mixins import GenCodeMixin, BaseMixin
from sqlalchemy.orm import validates 
from constants import PHONE, EMAIL
from ..accounts.models import *
from database import Base
import re

# class RestaurantVerificationCode(GenCodeMixin, Base):
#     __tablename__ = 'restaurant_verication_codes'

#     email = Column(String, unique=True, primary_key=True)

class EmailVerificationCode(GenCodeMixin, Base):
    '''Email Verification model'''
    __tablename__ = 'email_verication_codes'

    email = Column(String, unique=True, primary_key=True)

    @validates('email')
    def validate_email(self, key, value):
        assert re.search(EMAIL, value), 'invalid email format'
        return value

class SMSVerificationCode(GenCodeMixin, Base):
    __tablename__ = 'sms_verication_codes'

    phone = Column(String, unique=True, primary_key=True)

    @validates('phone')
    def validate_phone(self, key, value):
        assert re.search(PHONE, value), 'invalid phone format'
        return value

class RevokedToken(BaseMixin, Base):
    __tablename__ = 'revoked_tokens'

    jti = Column(String)

@event.listens_for(EmailVerificationCode, 'before_insert')
def delete_existing_value(mapper, connection, target):
    connection.execute("""DELETE FROM email_verication_codes WHERE email=:email""",{'email':target.email})

@event.listens_for(SMSVerificationCode, 'before_insert')
def delete_existing_value(mapper, connection, target):
    connection.execute("""DELETE FROM sms_verication_codes WHERE phone=:phone""",{'phone':target.phone})

# @event.listens_for(RestaurantVerificationCode, 'before_insert')
# def delete_existing_value(mapper, connection, target):
#     connection.execute("""DELETE FROM :table WHERE email=:email""",{'table':RestaurantVerificationCode.__tablename__, 'email':target.email})