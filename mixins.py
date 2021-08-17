from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declared_attr
import datetime

class BaseMixin(object):    
    status = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    @classmethod
    def c(cls):
        return [(c.name, c.type.python_type) for c in cls.__table__.columns]

class ImageMixin(BaseMixin):
    small = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    listquad = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    # @declared_attr
    # def p_id(cls):
    #     return Column('%s_id' % cls.p_name, Integer, ForeignKey( "%s.id" % cls.p_table ))

# class RatingMixin(BaseMixin):
#     value = Column(Float, nullable=False)

#     @declared_attr
#     def p_id(cls):
#         return Column('%s_id' % cls.p_name, Integer, ForeignKey( "%s.id" % cls.p_table ))

    # @declared_attr
    # def a_id(cls):
    #     return Column('%s_id' % cls.a_name, Integer, ForeignKey( "%s.id" % cls.a_table ))