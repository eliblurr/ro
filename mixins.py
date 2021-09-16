from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declared_attr
from passlib.hash import pbkdf2_sha256 as sha256
from utils import to_tsvector_ix, gen_code
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

class FullTextSearchMixin(object):
    # full text search here

    pass 
    # __ts_vector__ = to_tsvector_ix('english', *cols)
    # __table_args__ = (
    #     Index(
    #         'ix_tsv',
    #         to_tsvector_ix('english', 'title', 'symbol'),
    #         postgresql_using='gin'
    #         ),
    #         Index(
    #             'ix_full_text_search',
    #             __ts_vector__,
    #             postgresql_using='gin'
    #         ),
    #     )

    # __ts_vector__ = to_tsvector_ix('english', 'title', 'symbol')
    # __table_args__ = (
    #     Index(
    #         'ix_tsv',
    #         to_tsvector_ix('english', 'title', 'symbol'),
    #         postgresql_using='gin'
    #         ),
    #         Index(
    #             'idx_person_fts',
    #             __ts_vector__,
    #             postgresql_using='gin'
    #         ),
    #     )

    # option 1
    # @classmethod
    # def fulltext_search(cls, session, search_string, field):
    #     return session.query(cls).filter(func.to_tsvector('english', getattr(cls, field)).match(search_string, postgresql_regconfig='english')).all()




























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