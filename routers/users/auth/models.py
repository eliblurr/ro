from sqlalchemy import Column, String, Integer, event
from models import GenCodeMixin
from database import Base

class PasswordResetCode(GenCodeMixin, Base):
    __tablename__ = 'password_reset_codes'

    user_id = Column(Integer, unique=True)

class SMSVerificationCode(GenCodeMixin, Base):
    __tablename__ = 'sms_verication_codes'

    customer_id = Column(Integer, unique=True)

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    jti = Column(String)

@event.listens_for(PasswordResetCode, 'before_insert')
def delete_existing_value(mapper, connection, target):
    connection.execute("""DELETE FROM :table WHERE user_id=:user_id;""",{'table':PasswordResetCode.__tablename__, 'user_id':target.user_id})

@event.listens_for(SMSVerificationCode, 'before_insert')
def delete_existing_value(mapper, connection, target):
    connection.execute("""DELETE FROM :table WHERE customer_id=:customer_id;""",{'table':SMSVerificationCode.__tablename__,'customer_id':target.customer_id})