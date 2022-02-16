from sqlalchemy import Column, Integer, event, Unicode, Enum, select
from sqlalchemy_utils import generic_relationship
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import column_property
from sqlalchemy.orm import declared_attr
from services.aws import s3_delete
from utils import delete_path
from mixins import BaseMixin
from utils import today_str
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

# Remove from File System after_delete
@event.listens_for(Upload, 'after_delete')
def remove_file(mapper, connection, target):
    if target.url[:3]=='S3:':s3_delete(target.url[3:])
    else:delete_path(target.url[3:])

@declarative_mixin
class UploadProxy:
    def documents(self):
        return column_property(select(
                Upload.url
            ).where(
                Upload.object.is_type(self),
                Upload.object_id==self.id,
                Upload.upload_type=='document'
            ))

    def videos(self):
        return select(
                Upload.url
            ).where(
                Upload.object.is_type(self),
                Upload.object_id==self.id,
                Upload.upload_type=='video'
            )
    
    def images(self):
        return select(
                Upload.url
            ).where(
                Upload.object.is_type(self),
                Upload.object_id==self.id,
                Upload.upload_type=='image'
            )
    
    def audio(self):
        return select(
                Upload.url
            ).where(
                Upload.object.is_type(self),
                Upload.object_id==self.id,
                Upload.upload_type=='audio'
            )

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