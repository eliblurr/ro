from constants import Q_STR_X, SORT_STR_X, DT_X, Q_X, DT_Y, OPS
from inspect import Parameter, Signature, signature
from routers.media.models import Image as IM
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.sql import text
import re, datetime, shutil, os
from config import MEDIA_ROOT
from functools import wraps
from utils import gen_code, http_exception_detail, schema_to_model
from fastapi import Query, Depends
from typing import List
from PIL import Image
import utils, config as cfg

class CRUD:
    def __init__(self, model):
        self.model=model

    async def create(self, payload, db:Session, images=None):
        obj = self.model(**schema_to_model(payload))
        if images:
            obj.images.extend([
                IM(
                    detail =  f"{cfg.IMAGE_URL}{utils.create_image(image_b, cfg.IMAGE_ROOT)}", 
                    small = f"{cfg.IMAGE_URL}{utils.create_image(image_b, cfg.IMAGE_ROOT, cfg.SMALL)}",
                    listquad = f"{cfg.IMAGE_URL}{utils.create_image(image_b, cfg.IMAGE_ROOT, cfg.LISTQUAD)}",
                    thumbnail = f"{cfg.IMAGE_URL}{utils.create_image(image_b, cfg.IMAGE_ROOT, cfg.THUMBNAIL)}", 
                ) for image_b in [image.file.read() for image in images]
            ])
        db.add(obj)
        db.commit()
        db.refresh(obj) 
        return obj  
        
    async def read_by_id(self, id, db:Session):
        return db.query(self.model).filter(self.model.id==id).first()

    # to lower -> remove case sensitivity
    # .filter(
    #     func.lower(Example.string_col)
    #     .contains(search_string.lower(), autoescape=True)
    # )
    # .query.filter(Model.column.ilike("ganye"))
    # from sqlalchemy import func
    # user = models.User.query.filter(func.lower(User.username) == func.lower("GaNyE")).first()
    # FTS
    async def read(self, params, db:Session):
        # base = db.query(self.model)
        # from sqlalchemy import func
        # ext_filters = {x:params[x]if params[x]!='null' else None for x in params if x not in ["offset", "limit", "q", "sort", "action"] and params[x] is not None}
        # # ext_filters = [f'{self.model.x}']
        # # base = base.filter_by(**ext_filters)
        # # f'{self.model.__table__.c[k].ilike(v if v is not None else None)}'
        # a = [f'{self.model.__table__.c[k].ilike(v if v is not None else None)}' for k,v in ext_filters.items()]
        # if a:
        #     base = base.filter(and_(text(*a)))
        # # print(base)
        # return
        base = db.query(self.model)
        dt_cols = [col[0] for col in self.model.c() if col[1]==datetime.datetime]
        dte_filters = {x:params[x] for x in params if x in dt_cols and params[x] is not None}
        ext_filters = {x:params[x] if params[x]!='null' else None for x in params if x not in ["offset", "limit", "q", "sort", "action", *dt_cols] and params[x] is not None}
        dte_filters = [ f'{self.model.__table__.c[k]} {OPS.get(val.split(":", 1)[0], "==")} "{val.split(":", 1)[1]}"' if re.search(DT_Y, val) else f'{self.model.__table__.c[k]} == {val}' for k,v in dte_filters.items() for val in v]

        base = base.filter_by(**ext_filters)

        if dte_filters:
            base = base.filter(text(' AND '.join(dte_filters)))
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
            
    async def update(self, id, payload, db:Session, images=None):
        rows = db.query(self.model).filter(self.model.id==id).update(schema_to_model(payload, True), synchronize_session="fetch")
        db.commit()
        return await self.read_by_id(id, db)

    async def delete(self, id, db:Session):
        rows = db.query(self.model).filter(self.model.id==id).delete(synchronize_session=False)
        db.commit()
        return rows

    async def bk_create(self, payload, db:Session):
        db.add_all([self.model(**payload.dict()) for payload in payload])
        db.commit()

    async def bk_update(self, payload, db:Session, **kwargs):
        rows = db.query(self.model).filter_by(**kwargs).update(payload.dict(exclude_unset=True), synchronize_session="fetch")
        db.commit()
        return rows

    async def bk_delete(self, ids:list, db:Session):
        # deleted_objects = User.__table__.delete().where(User.id.in_([1, 2, 3]))
        # session.execute(deleted_objects)
        # session.commit()
        rows = db.query(self.model).filter(self.model.id.in_(ids)).delete(synchronize_session=False)
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

class Folder:
    def __init__(self, base_dir, name):
        self.base_dir = base_dir
        self.name = name

    def __call__(self):
        return os.mkdir(f'{self.base_dir}/{self.name}')

    def delete(self):
        return shutil.rmtree(f'{self.base_dir}/{self.name}')

    def rename(self, name):
        try:
            os.rename(self.name, new_name)
        except Exception as e:
            print(e.__class__)
        else:
            self.name = name

    def path(self):
        return f'{self.base_dir}/{self.name}'

'''
    NOTES
    # 1. exact filter *
    # 2. like AND filter -> q k:v *
    # 3. like OR filter -> q v *
    # 4. date filter
    # 5. sort *
    # 6. offset & limit *

    # try:
    #     db.add(obj)
    # except:
    #     db.rollback()
    # else:
    #     db.commit()
    #     db.refresh(obj) 

    cols = [col[0] for col in self.model.c()]
    vals =  ['string1', 'string2']
    for val in vals:
        n_vals = [self.model.__table__.c[col].like('%' + str(val) + '%') for col in cols]
    x = [ or_(*[self.model.__table__.c[col].like('%' + str(val) + '%') for col in cols]) for val in vals ]
    base = base.filter(and_(*x))

    dte_filters = [ f'{self.model.__table__.c[k]} {OPS.get(val.split(":", 1)[0], "==")} {val.split(":", 1)[1]}' if re.search(DT_Y, val) else f'{self.model.__table__.c[k]} == {val}' for k,v in dte_filters.items() for val in v]
    for val in v for k,v in dte_filters.items()
        for val in v:
            if re.search(DT_Y, val):
                op, val = val.split(':', 1)
                q = f'{self.model.__table__.c[k]} {OPS.get(op, "==")} {val}'
            else:
                q = f'{self.model.__table__.c[k]} == {val}'
'''