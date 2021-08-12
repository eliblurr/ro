from constants import Q_STR_X, SORT_STR_X, DT_X, Q_X, DT_Y
from inspect import Parameter, Signature, signature
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.sql import text
from functools import wraps
from fastapi import Query
from typing import List
import re, datetime

class CRUD:
    def __init__(self, model):
        self.model=model

    async def create(self, payload, db:Session, images=None):
        obj = self.model(**payload.dict())
        # if images:
        #     obj.images = ''
        db.add(obj)
        db.commit()
        db.refresh(obj) 
        return obj  

    async def read_by_id(self, id, db:Session):
        return db.query(self.model).filter(self.model.id==id).first()

    async def read(self, params, db:Session):
        base = db.query(self.model)
        ext_filters = {x:params[x] for x in params if x not in {"offset", "limit", "q", "sort", "action"} and params[x] is not None and self.model.__table__.c[x].type.python_type != datetime.datetime}
        base = base.filter_by(**ext_filters)
        if params['sort']:
            sort = [f'{item[1:]} desc' if re.search(SORT_STR_X, item) else f'{item} asc' for item in params['sort']]
            base = base.order_by(text(*sort))
        if params['q']:
            q_and, q_or = [], []
            [q_and.append(item) if re.search(Q_STR_X, item) else q_or.append(item) for item in params['q']]
            q_and = [self.model.__table__.c[item.split(':')[0]].like('%' + str(item.split(':')[1]) + '%') for item in q_and]
            if db.bind.dialect.name=='postgres':
                q_or = [self.model.__ts_vector__.match(item) for item in q_or]
            else:
                q_or = [ or_(*[self.model.__table__.c[col].like('%' + str(val) + '%') for col in [col[0] for col in self.model.c()]]) for val in q_or ]
            base = base.filter(and_(*q_and)).filter(and_(*q_or))
             
        data = base.offset(params['offset']).limit(params['limit']).all()
        return {'bk_size':base.count(), 'pg_size':data.__len__(), 'data':data}

        '''////////////////////////////////////'''

        dte_filters = {x:params[x] for x in params if self.model.__table__.c[x].type.python_type == datetime.datetime and params[x] is not None}
        # dte_filters = {x:params[x] for x in params if x not in {"offset", "limit", "q", "sort", "action"} and isinstance(self.model.__table__.c[x].type.python_type, datetime.datetime) and params[x] is not None}
        # [f'{k} < {v}' if op=='lt' else f'{k} <= {v}' if op=='lte' else f'{k} > {v}' if op=='gt' else f'{k} >= {v}' if op=='gte' else '=' for k,v in dte_filters if re.search(DT_Y, v)]

        [f'{k} = {v}' for k,v in dte_filters if not re.search(DT_Y, v)]
        for k,v in dte_filters:
            if re.search(DT_Y, v):
                op, v = v.split(':')
                [f'{k} < {v}' if op=='lt' else f'{k} <= {v}' if op=='lte' else f'{k} > {v}' if op=='gt' else f'{k} >= {v}' if op=='gte' else '=' for k,v in dte_filters]
                op = 'lt|lte|gt|gte'
                pass
            filter(and_(

            ))

        

    async def update(self, id, payload, db:Session, images=None):
        db.query(self.model).filter(self.model.id==id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await self.read_by_id(id, db)

    async def delete(self, id, db:Session, im_id=None):
        rows = db.query(self.model).filter(self.model.id==id).delete()
        db.commit()
        return rows

class ContentQueryChecker:
    def __init__(self, cols=None, actions=None):
        self._cols = cols
        self._actions = actions
    
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        sig = signature(wrapper)
        params = list(sig._parameters.values())
        del params[-1]
        sort_str = "|".join([f"{x[0]}|-{x[0]}" for x in self._cols]) if self._cols else None
        q_str = "|".join([x[0] for x in self._cols]) if self._cols else None
        if self._cols:
            params.extend([Parameter(param[0], Parameter.KEYWORD_ONLY, annotation=param[1], default=Query(None)) for param in self._cols if param[1]!=datetime.datetime])
            params.extend([
                Parameter(param[0], Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex=DT_X)) for param in self._cols if param[1]==datetime.datetime
            ])
        params.extend([
            Parameter('offset', Parameter.KEYWORD_ONLY, annotation=int, default=Query(0, gte=0)),
            Parameter('limit', Parameter.KEYWORD_ONLY, annotation=int, default=Query(100, gt=0)),
            Parameter('q', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex=Q_X.format(cols=f'({q_str})') if q_str else '^[\w]+$|^[\w]+:[\w]+$')),
            Parameter('sort', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex=sort_str if sort_str else '(^-)?\w')),])  
        if self._actions:
            params.extend([Parameter('action', Parameter.KEYWORD_ONLY, annotation=str, default=Query(None))])
        wrapper.__signature__ = Signature(params)
        return wrapper

'''
    NOTES
    # 1. exact filter *
    # 2. like AND filter -> q k:v *
    # 3. like OR filter -> q v *
    # 4. date filter
    # 5. sort *
    # 6. offset & limit *

    cols = [col[0] for col in self.model.c()]
    vals =  ['string1', 'string2']
    for val in vals:
        n_vals = [self.model.__table__.c[col].like('%' + str(val) + '%') for col in cols]
    x = [ or_(*[self.model.__table__.c[col].like('%' + str(val) + '%') for col in cols]) for val in vals ]
    base = base.filter(and_(*x))
'''