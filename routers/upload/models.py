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

class UploadProxy:

    def _base_(self, db, type_:str, offset:int=0, limit:int=100):
        return db.query(
            Upload.url
        ).filter(
            Upload.object==self,
            Upload.upload_type==type_
        ).order_by(
            desc(Upload.created)
        ).offset(offset).limit(limit).all()
    
    def documents(self, db, offset:int=0, limit:int=100):
        return self._base_(self, db, 'document', offset, limit)

    def videos(self, db, offset:int=0, limit:int=100):
        return self._base_(self, db, 'video', offset, limit)

    def audio(self, db, offset:int=0, limit:int=100):
        return self._base_(self, db, 'audio', offset, limit)

    def images(self, db, offset:int=0, limit:int=100):
        return self._base_(self, db, 'image', offset, limit)