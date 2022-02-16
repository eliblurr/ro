from pydantic import BaseModel, confloat
from typing import Optional, List
import datetime

class RatingBase(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    rating: confloat(ge=0, le=5)

    class Config:
        orm_mode = True

class CreateRating(RatingBase):
    meal_id: int
    author_id: Optional[int]

class Rating(RatingBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime

class RatingList(BaseModel):
    bk_size: int
    pg_size: int
    data: List[Rating]