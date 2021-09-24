from utils import gen_code, http_exception_detail, schema_to_model, str_to_datetime, create_image
from constants import Q_STR_X, SORT_STR_X, DT_X, Q_X, DT_Y, OPS
from inspect import Parameter, Signature, signature
from fastapi import Query, Depends, HTTPException
from routers.media.models import Image as IM
from sqlalchemy.exc import IntegrityError
from exceptions import MaxOccurrenceError
from sqlalchemy import and_, or_, func
import re, datetime, shutil, os, enum
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from config import MEDIA_ROOT
from functools import wraps
from typing import List
from PIL import Image
import config as cfg

class CRUD:
    def __init__(self, model):
        self.model=model

    async def create(self, payload, db:Session, images=None):
        try:
            obj = self.model(**schema_to_model(payload))
            if images:
                obj.images.extend([
                    IM(
                        detail =  f"{cfg.IMAGE_URL}{create_image(image_b, cfg.IMAGE_ROOT)}", 
                        small = f"{cfg.IMAGE_URL}{create_image(image_b, cfg.IMAGE_ROOT, cfg.SMALL)}",
                        listquad = f"{cfg.IMAGE_URL}{create_image(image_b, cfg.IMAGE_ROOT, cfg.LISTQUAD)}",
                        thumbnail = f"{cfg.IMAGE_URL}{create_image(image_b, cfg.IMAGE_ROOT, cfg.THUMBNAIL)}", 
                    ) for image_b in [image.file.read() for image in images]
                ])
            db.add(obj)
            db.commit()
            db.refresh(obj) 
            return obj  
        except IntegrityError as e:
            print(e)
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
        except MaxOccurrenceError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))
        
    async def read_by_id(self, id, db:Session):
        try:
            return db.query(self.model).filter(self.model.id==id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

    async def read(self, params, db:Session):
        try:
            base = db.query(self.model)
            dt_cols = [col[0] for col in self.model.c() if col[1]==datetime.datetime]
            ex_cols = [col[0] for col in self.model.c() if col[1]==int or col[1]==bool or issubclass(col[1], enum.Enum)]
            
            dte_filters = {x:params[x] for x in params if x in dt_cols and params[x] is not None} 
            ex_filters = {x:params[x] for x in params if x  in ex_cols and  params[x] is not None}
            ext_filters = {x:params[x] for x in params if x not in ["offset", "limit", "q", "sort", "action", *dt_cols, *ex_cols] and params[x] is not None}
            filters = [ getattr(self.model, k).match(v) if v!='null' else getattr(self.model, k)==None for k,v in ext_filters.items()]
            filters.extend([getattr(self.model, k)==v if v!='null' else getattr(self.model, k)==None for k,v in ex_filters.items()])
            filters.extend([
                getattr(self.model, k) >= str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='gte'
                else getattr(self.model, k) <= str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='lte'
                else getattr(self.model, k) > str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='gt'
                else getattr(self.model, k) < str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='lt'
                else getattr(self.model, k) == str_to_datetime(val)
                for k,v in dte_filters.items() for val in v 
            ])

            base = base.filter(*filters)

            if params['sort']:
                sort = [f'{item[1:]} desc' if re.search(SORT_STR_X, item) else f'{item} asc' for item in params['sort']]
                base = base.order_by(text(*sort))
            if params['q']:
                q_or, fts = [], []
                [ q_or.append(item) if re.search(Q_STR_X, item) else fts.append(item) for item in params['q'] ]
                q_or = or_(*[getattr(self.model, q.split(':')[0]).match(q.split(':')[1]) if q.split(':')[1]!='null' else getattr(self.model, q.split(':')[0])==None for q in q_or])
                fts = or_(*[getattr(self.model, col[0]).ilike(f'%{val}%') for col in self.model.c() if col[1]==str for val in fts])
                
                base = base.filter(fts).filter(q_or)
            data = base.offset(params['offset']).limit(params['limit']).all()
            return {'bk_size':base.count(), 'pg_size':data.__len__(), 'data':data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
            
    async def update(self, id, payload, db:Session, images=None):
        try:
            rows = db.query(self.model).filter(self.model.id==id).update(schema_to_model(payload, True), synchronize_session="fetch")
            db.commit()
            return await self.read_by_id(id, db)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
        except MaxOccurrenceError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

    async def delete(self, id, db:Session):
        try:
            rows = db.query(self.model).filter(self.model.id==id).delete(synchronize_session=False)
            db.commit()
            return f"{rows} row(s) deleted"
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

    async def bk_create(self, payload, db:Session):
        try:
            db.add_all([self.model(**payload.dict()) for payload in payload])
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

    async def bk_update(self, payload, db:Session, **kwargs):
        try:
            rows = db.query(self.model).filter_by(**kwargs).update(payload.dict(exclude_unset=True), synchronize_session="fetch")
            db.commit()
            return rows
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

    async def bk_delete(self, ids:list, db:Session):
        try:
            rows = db.query(self.model).filter(self.model.id.in_(ids)).delete(synchronize_session=False)
            db.commit()
            return f"{rows} row(s) deleted"
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
        except MaxOccurrenceError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

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
            # fts = or_(*[self.model.__ts_vector__.match(search_string) for search_string in fts])
            # ext filters as list -> (X==1 OR X==2) AND (Y==1 OR Y==2)

            filters = [ getattr(self.model, k).match(item) if item!='null' else getattr(self.model, k)==None for k,v in ext_filters.items() for item in v ]
            filters.extend([getattr(self.model, k)==item if item!='null' else getattr(self.model, k)==None for k,v in ex_filters.items() for item in v ])
            filters.extend([
                getattr(self.model, k) >= str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='gte'
                else getattr(self.model, k) <= str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='lte'
                else getattr(self.model, k) > str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='gt'
                else getattr(self.model, k) < str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='lt'
                else getattr(self.model, k) == str_to_datetime(val)
                for k,v in dte_filters.items() for val in v 
            ])
# base = base.filter(text(' AND '.join(dte_filters)))
        # dte_filters = [ f'{getattr(self.model, k)} {OPS.get(val.split(":", 1)[0], "==")} "{val.split(":", 1)[1]}"' if re.search(DT_Y, val) else f'{getattr(self.model, k)} == {val}' for k,v in dte_filters.items() for val in v]

    # q_or = [self.model.__table__.c[q.split(':')[0]].match(q.split(':')[1]) if q.split(':')[1]!='null' else self.model.__table__.c[q.split(':')[0]]==None for q in q_or]
                
            # if db.bind.dialect.name=='postgresql':
            # #     fts = [self.model.__ts_vector__.match(f'{search_string} & us') for search_string in fts]
            # #     fts = [self.model.__table__.c[col].ilike('%' + str(val) + '%') for col in [col[0] for col in self.model.c()] for val in fts]
            #     fts = or_(*[self.model.__ts_vector__.match(search_string) for search_string in fts])
            # else:

    # text(' AND '.join(dte_filters))

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

    dte_filters = [ f'{getattr(self.model, k)} {OPS.get(val.split(":", 1)[0], "==")} {val.split(":", 1)[1]}' if re.search(DT_Y, val) else f'{getattr(self.model, k)} == {val}' for k,v in dte_filters.items() for val in v]
    for val in v for k,v in dte_filters.items()
        for val in v:
            if re.search(DT_Y, val):
                op, val = val.split(':', 1)
                q = f'{getattr(self.model, k)} {OPS.get(op, "==")} {val}'
            else:
                q = f'{getattr(self.model, k)} == {val}'

    # q_and, q_or = [], []
    # [q_and.append(item) if re.search(Q_STR_X, item) else q_or.append(item) for item in params['q']]
    # q_and = [self.model.__table__.c[item.split(':')[0]].ilike('%' + str(item.split(':')[1]) + '%') for item in q_and]
    # if db.bind.dialect.name=='postgres':
    #     q_or = [self.model.__ts_vector__.match(item) for item in q_or]
    # else:
        # q_or = [ or_(*[self.model.__table__.c[col].ilike('%' + str(val) + '%') for col in [col[0] for col in self.model.c()]]) for val in q_or ]
    # base = base.filter(and_(*q_and)).filter(and_(*q_or))

    class UnAcceptedValueError(Exception):   
    def __init__(self, data):    
        self.data = data
    def __str__(self):
        return repr(self.data)

    Total_Marks = int(input("Enter Total Marks Scored: "))
    try:
        Num_of_Sections = int(input("Enter Num of Sections: "))
        if(Num_of_Sections < 1):
            raise UnAcceptedValueError("Number of Sections can't be less than 1")
    except UnAcceptedValueError as e:
        print ("Received error:", e.data)
'''