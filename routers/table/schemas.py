from typing import Optional, List
from pydantic import BaseModel, conint
import datetime

class TableBase(BaseModel):
    code: Optional[str]
      
class CreateTable(TableBase):
    restaurant_id: int
    
class UpdateTable(BaseModel):
    code: Optional[str]
    status: Optional[bool]
    restaurant_id: Optional[int]

class Table(TableBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True

class TableList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Table]