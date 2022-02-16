from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, Float, Index, types, Unicode
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import TSVECTOR
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy_utils import TSVectorType
from utils import to_tsvector, gen_code
from sqlalchemy.sql import func
from database import engine
import datetime

from ctypes import File

class BaseMethodMixin(object):
    @classmethod
    def c(cls):
        return [
            (c.name, c.type.python_type) for c in cls.__table__.columns if not isinstance(c.type, File)

        ]
    # @classmethod
    # def c(cls):
    #     return [(c.name, c.type.python_type) if c.name!='__ts_vector__' else (c.name, None) for c in cls.__table__.columns]
    # return [
        #     (c.name, c.type.python_type) if not isinstance(c.type, File) else (c.name, str) for c in cls.__table__.columns
        # ]

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
    if engine.name == 'postgresql':
        @declared_attr
        def __ts_vector__(cls):
            return func.to_tsvector('english', cls.title)

        @declared_attr
        def __table_args__(cls):
            return (
                Index(
                    'ix_%s_ts_vector_' % cls.__tablename__, 
                    cls.__ts_vector__,
                    postgresql_using='gin'
                ),
            )

# class UploadMixin(object):
#     __abstract__ = True
    
#     @declared_attr
#     def documents(cls):
#         return 
#         UserVote.objects.get(voter=voter, object_id=self.id)
#         self.documents
# Find the event we just made.
# session.query(Event).filter_by(object=user).first()

# # Find any events that are bound to users.
# session.query(Event).filter(Event.object.is_type(User)).all()


'''
Working POSTGRESQL QUERY -> -- select * from currencies WHERE to_tsvector(title ||' '|| id ||' '|| status) @@ to_tsquery('true')
# class TSVector(types.TypeDecorator):
#     impl = TSVECTOR

# import sqlalchemy as sa
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship, column_property
# from sqlalchemy.sql.expression import cast
# from sqlalchemy.dialects import postgresql

# print(dir(postgresql))


# def create_tsvector(*args):
#     exp = args[0]
#     for e in args[1:]:
#         exp += ' ' + e
#     # s = " || ' ' || ".join(args)
#     # print(s)
#     return func.to_tsvector('english', exp)

# def to_tsvector_ix(*columns):
#     s = " || ' ' || ".join(columns)

#     print(s)


#     return func.to_tsvector('english', sa.text(s))
#     # s = " || ' ' || ".join(columns)
#     # return sa.sql.func.to_tsvector(lang, sa.text(s))
# __ts_vector__ = db.Column(TSVector(),db.Computed(
#          "to_tsvector('english', title || ' ' || description)",
#          persisted=True))
#     __table_args__ = (Index('ix_video___ts_vector__',
#           __ts_vector__, postgresql_using='gin'),)

 # @declared_attr
        # def __ts_vector__(cls):
        # __ts_vector__ = func.to_tsvector('english', 'title || ' ' || symbol')

        # __ts_vector__ = create_tsvector(
        #     cast(func.coalesce(title, ''), postgresql.TEXT)
        # )

# return Column(TSVector(), default=func.to_tsvector('english', sa.text(f""" "title" ||' '|| "id" ||' '|| "status" """) ) )

            # return create_tsvector(
            #     cast(func.coalesce(cls.title, ''), postgresql.TEXT)
            # )

            # return func.to_tsvector('english', sa.text(f""" "title" ||' '|| "id" ||' '|| "status" """))
            # 


# cast(func.coalesce(cls.title, ''), postgresql.TEXT)
# select * from currencies WHERE to_tsvector("title" ||' '|| "id" ||' '|| "status") @@ to_tsquery('usd')
                                           # "symbol" || ' ' || "title" || ' ' || "id"
         
        # @declared_attr
        # def __ts_vector__(cls):
        #     return column_property(func.to_tsvector('pg_catalog.english', 'title'))
        # #     return sa.sql.func.to_tsvector('pg_catalog.english', sa.text(*cls.__ftcols__))
        #     # return to_tsvector('pg_catalog.english', *cls.__ftcols__)
        #     # title || ' ' || description
        #     return Column(TSVector(), default = "func.to_tsvector('pg_catalog.english', cls.title || ' ' || cls.symbol)")





# class TSVectorType(types.TypeDecorator):
#     """
#     .. note::

#         This type is PostgreSQL specific and is not supported by other
#         dialects.

#     Provides additional functionality for SQLAlchemy PostgreSQL dialect's
#     TSVECTOR_ type. This additional functionality includes:

#     * Vector concatenation
#     * regconfig constructor parameter which is applied to match function if no
#       postgresql_regconfig parameter is given
#     * Provides extensible base for extensions such as SQLAlchemy-Searchable_

#     .. _TSVECTOR:
#         http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#full-text-search

#     .. _SQLAlchemy-Searchable:
#         https://www.github.com/kvesteri/sqlalchemy-searchable

#     ::

#         from sqlalchemy_utils import TSVectorType


#         class Article(Base):
#             __tablename__ = 'user'
#             id = sa.Column(sa.Integer, primary_key=True)
#             name = sa.Column(sa.String(100))
#             search_vector = sa.Column(TSVectorType)


#         # Find all articles whose name matches 'finland'
#         session.query(Article).filter(Article.search_vector.match('finland'))


#     TSVectorType also supports vector concatenation.

#     ::


#         class Article(Base):
#             __tablename__ = 'user'
#             id = sa.Column(sa.Integer, primary_key=True)
#             name = sa.Column(sa.String(100))
#             name_vector = sa.Column(TSVectorType)
#             content = sa.Column(sa.String)
#             content_vector = sa.Column(TSVectorType)

#         # Find all articles whose name or content matches 'finland'
#         session.query(Article).filter(
#             (Article.name_vector | Article.content_vector).match('finland')
#         )

#     You can configure TSVectorType to use a specific regconfig.
#     ::

#         class Article(Base):
#             __tablename__ = 'user'
#             id = sa.Column(sa.Integer, primary_key=True)
#             name = sa.Column(sa.String(100))
#             search_vector = sa.Column(
#                 TSVectorType(regconfig='pg_catalog.simple')
#             )


#     Now expression such as::


#         Article.search_vector.match('finland')


#     Would be equivalent to SQL::


#         search_vector @@ to_tsquery('pg_catalog.simgle', 'finland')

#     """
#     impl = TSVECTOR
#     cache_ok = True

#     class comparator_factory(TSVECTOR.Comparator):
#         def match(self, other, **kwargs):
#             if 'postgresql_regconfig' not in kwargs:
#                 if 'regconfig' in self.type.options:
#                     kwargs['postgresql_regconfig'] = (
#                         self.type.options['regconfig']
#                     )
#             return TSVECTOR.Comparator.match(self, other, **kwargs)

#         def __or__(self, other):
#             return self.op('||')(other)

#     def __init__(self, *args, **kwargs):
#         """
#         Initializes new TSVectorType

#         :param *args: list of column names
#         :param **kwargs: various other options for this TSVectorType
#         """
#         self.columns = args
#         self.options = kwargs
#         super(TSVectorType, self).__init__(*args, **kwargs)













# @declared_attr
    # def __ts_vector__(cls):
    #     if engine.name ==  'postgres':
    #         return Column(TSVectorType(*cls.__ftcols__))
    #     return Column(String, default='database engine is not postgres')

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

'''