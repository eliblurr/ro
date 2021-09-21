from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, Float, Index, types
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import TSVECTOR
from passlib.hash import pbkdf2_sha256 as sha256
from utils import to_tsvector, gen_code
import datetime

class BaseMethodMixin(object):
    @classmethod
    def c(cls):
        return [(c.name, c.type.python_type) for c in cls.__table__.columns]

class BaseMixin(BaseMethodMixin):    
    status = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class HashMethodMixin(object):
    def generate_hash(data):
        return sha256.hash(data)
    
    def verify_hash(self, data, hash):
        return sha256.verify(data, hash)

class GenCodeMixin(object):
    code = Column(String, unique=False, default=gen_code)

class TSVector(types.TypeDecorator):
    impl = TSVECTOR

class FullTextSearchMixin(object):
    @declared_attr
    def __ts_vector__(cls):
        return to_tsvector(*cls.__ftcols__)
        # Column(TSVector(), Computed("to_tsvector('english', title || ' ' || description)", persisted=True))

    @declared_attr
    def __table_args__(cls):
        return (
            Index(
                'ix_%s__ts_vector__' % cls.__tablename__, 
                cls.__ts_vector__, 
                postgresql_using='gin'
            ),
        )

    # @classmethod
    # def search_query(cls, session, search_string):
    #     return session.query(cls).filter(cls.__ts_vector__.match(search_string)).subquery()
        # session.query(cls).
        # return session.query(cls).filter(func.to_tsvector('english', getattr(cls, field)).match(search_string, postgresql_regconfig='english')).all()




























# class RatingMixin(BaseMixin):
#     value = Column(Float, nullable=False)

#     @declared_attr
#     def p_id(cls):
#         return Column('%s_id' % cls.p_name, Integer, ForeignKey( "%s.id" % cls.p_table ))

    # @declared_attr
    # def a_id(cls):
    #     return Column('%s_id' % cls.a_name, Integer, ForeignKey( "%s.id" % cls.a_table ))

# class ImageMixin(BaseMixin):
#     small = Column(String, nullable=True)
#     detail = Column(String, nullable=True)
#     listquad = Column(String, nullable=True)
#     thumbnail = Column(String, nullable=True)