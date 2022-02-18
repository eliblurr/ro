from sqlalchemy import Column, Integer, event, Unicode, Enum, select, desc, asc
from sqlalchemy_utils import generic_relationship
from utils import today_str, async_remove_file
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import column_property
from sqlalchemy.orm import declared_attr
from services.aws import s3_delete
from utils import delete_path
from mixins import BaseMixin
from database import Base
from ctypes import File
import enum

class UploadType(str, enum.Enum):
    document='document'
    audio='audio'
    video='video'
    image='image'
    
class Upload(BaseMixin, Base):
    '''Upload Model'''
    __tablename__ = "uploads"

    url = Column(File(upload_to=f'{today_str()}'), nullable=False)
    upload_type = Column(Enum(UploadType), nullable=False)

    object_type = Column(Unicode(255))
    object_id = Column(Integer, nullable=False)
    object = generic_relationship('object_type', 'object_id')

@event.listens_for(Upload, 'after_delete')
def remove_file(mapper, connection, target):
    if target.url:async_remove_file(target.url)

from sqlalchemy.ext.declarative import declared_attr

# @declarative_mixin
class UploadProxy(object):
    
    def documents(self, db, offset:int=0, limit:int=100):
        return db.query(
            Upload.url
        ).filter(
            Upload.object==self,
            Upload.upload_type=='document'
        ).order_by(
            desc(Upload.created)
        ).offset(offset).limit(limit).all()
        
        # .offset(params['offset']).limit(params['limit'])
        # select(Upload.url).where(
        #     Upload.object==self,
        #     Upload.upload_type=='document'
        # ).order_by(
        #     desc(Upload.__table__.c.created)
        # )

    # @declared_attr
    # def documents(cls):
    #     print(cls)
    #     return column_property(select(
    #             Upload.url
    #         ).where(
    #             Upload.upload_type=='document'
    #         ).order_by(
    #             desc(Upload.__table__.c.created)
    #         )
    #         .scalar_subquery()
    #     )

        # .where(
        #         Upload.object.is_type(cls),
        #         Upload.object_id==cls.id,
        #         Upload.upload_type=='document'
        #     )

    # def videos(self):
    #     return column_property(select(
    #             Upload.url
    #         ).where(
    #             Upload.object.is_type(self),
    #             Upload.object_id==self.id,
    #             Upload.upload_type=='video'
    #         ).order_by(
    #             desc(Upload.__table__.c.created)
    #         )
    #     )
    
    # def images(self):
    #     return column_property(select(
    #             Upload.url
    #         ).where(
    #             Upload.object.is_type(self),
    #             Upload.object_id==self.id,
    #             Upload.upload_type=='image'
    #         ).order_by(
    #             desc(Upload.__table__.c.created)
    #         )
    #     )
    
    # def audio(self):
    #     return column_property(select(
    #             Upload.url
    #         ).where(
    #             Upload.object.is_type(self),
    #             Upload.object_id==self.id,
    #             Upload.upload_type=='audio'
    #         ).order_by(
    #             desc(Upload.__table__.c.created)
    #         )
    #     )

    # def add():
    #     pass

    # def remove(self, id):
    #     pass

    # @declared_attr
    # def uploads(self):
    #     return column_property(
    #         select(
    #             Upload.url
    #         ).where(
    #             Upload.object.is_type(self),
    #             Upload.object_id==self.id,
    #         )
    #     )