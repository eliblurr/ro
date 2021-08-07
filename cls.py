from inspect import Parameter, Signature, signature
from sqlalchemy.orm import Session
from functools import wraps
from fastapi import Query
from typing import List


class CRUD:
    def __init__(self, model):
        self.model=model

    async def create(self, payload, db:Session, images=None):
        obj = self.model(**payload.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj) 
        return obj  

    async def read_by_id(self, id, db:Session):
        return db.query(self.model).filter(self.model.id==id).first()

    async def read(self, params, db:Session, child=None):
        # q = like search[split@:] and text_search
        # sort = index 0 if - desc else asc
        # search:str=None, value:str=None, skip:int=0, limit:int=100
        base = db.query(self.model)
        if search and value:
            try:
                base = base.filter(self.model.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                pass
        return base.offset(offset).limit(limit).all()

    async def update(self, id, payload, db:Session, images=None):
        db.query(self.model).filter(self.model.id==id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await self.read_by_id(id, db)

    async def delete(self, id, db:Session, im_id=None):
        rows = db.query(self.model).filter(self.model.id==id).delete()
        db.commit()
        return rows

class Page:
    def __init__(self, page:int=Query(1, gt=0), page_size:int=Query(100, gte=0)):
        self.page = page
        self.page_size = page_size
        self.offset = self.page_size
        self.skip = (self.page_size*self.page) - self.page_size

class ContentQueryChecker:
    def __init__(self, cols, actions):
        self._cols = cols
        self._actions = actions
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        sig = signature(wrapper)
        params = list(sig._parameters.values())
        del params[-1]
        params.extend([Parameter(param[0], Parameter.KEYWORD_ONLY, annotation=param[1], default=Query(None)) for param in self._cols])
        params.extend([
            Parameter('offset', Parameter.KEYWORD_ONLY, annotation=int, default=Query(None, gte=0)),
            Parameter('limit', Parameter.KEYWORD_ONLY, annotation=int, default=Query(None, gt=0)),
            Parameter('q', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex='^[\w]+$|^[\w]+:[\w]+$')),
            Parameter('sort', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex='(^-)?\w')),])  
        wrapper.__signature__ = Signature(params)
        return wrapper