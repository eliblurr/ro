from typing import Optional, List
from pydantic import BaseModel
import datetime

class CurrencyBase(BaseModel):
    title: str
    symbol: Optional[str]
    
class CreateCurrency(CurrencyBase):
    status: Optional[bool]

class UpdateCurrency(BaseModel):
    title: Optional[str]
    symbol: Optional[str]
    status: Optional[bool]

class Currency(CurrencyBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class CurrencyResponse(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Currency]