from sqlalchemy import Column, String, Integer, event
from mixins import GenCodeMixin, BaseMixin
from sqlalchemy.orm import validates 
from ..accounts.models import *
from constants import PHONE
from database import Base
import re

class PasswordResetCode(GenCodeMixin, Base):
    __tablename__ = 'password_reset_codes'

    user_id = Column(Integer, unique=True, primary_key=True)

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

@event.listens_for(PasswordResetCode, 'before_insert')
def delete_existing_value(mapper, connection, target):
    connection.execute("""DELETE FROM :table WHERE user_id=:user_id;""",{'table':PasswordResetCode.__tablename__, 'user_id':target.user_id})

@event.listens_for(SMSVerificationCode, 'before_insert')
def delete_existing_value(mapper, connection, target):
    connection.execute("""DELETE FROM :table WHERE phone=:phone;""",{'table':SMSVerificationCode.__tablename__,'phone':target.phone})