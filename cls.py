from utils import gen_code, http_exception_detail, schema_to_model, str_to_datetime, create_image
from exceptions import MaxOccurrenceError, FileNotSupported, UploadNotAllowed
from constants import Q_STR_X, SORT_STR_X, DT_X, Q_X, DT_Y, OPS
from sqlalchemy.orm.relationships import RelationshipProperty
from inspect import Parameter, Signature, signature
import re, datetime, shutil, os, enum, pathlib, os
from fastapi import Query, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func
from services.aws import s3_upload
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from config import UPLOAD_ROOT
from functools import wraps
from typing import List
from io import BytesIO
from PIL import Image
import config as cfg

class CRUD:
    def __init__(self, model):
        self.model=model

    async def create(self, payload, db:Session, **kwargs):
        try:
            obj = self.model(**schema_to_model(payload))
            [setattr(obj, k, v) for k, v in kwargs.items()]
            db.add(obj)
            db.commit()
            db.refresh(obj) 
            return obj  
        except IntegrityError as e:
            # raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except MaxOccurrenceError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except AssertionError as e:
            raise HTTPException(status_code=400, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))
        
    async def read_by_id(self, id, db:Session):
        try:
            return db.query(self.model).get(id)
            # .filter(self.model.id==id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))

    async def read(self, params, db:Session, related_name:str=None, resource_id:int=None):
        try:
            model_to_filter, base = self._base(db, params['fields'], related_name=related_name, resource_id=resource_id)             
            dt_cols = [col[0] for col in model_to_filter.c() if col[1]==datetime.datetime]
            ex_cols = [col[0] for col in model_to_filter.c() if col[1]==int or col[1]==bool or issubclass(col[1], enum.Enum)]
            dte_filters = {x:params[x] for x in params if x in dt_cols and params[x] is not None} 
            ex_filters = {x:params[x] for x in params if x  in ex_cols and  params[x] is not None}
            ext_filters = {x:params[x] for x in params if x not in ["offset", "limit", "q", "sort", "action", "fields", *dt_cols, *ex_cols] and params[x] is not None}
            filters = [ getattr(model_to_filter, k).match(v) if v!='null' else getattr(model_to_filter, k)==None for k,v in ext_filters.items()]
            filters.extend([getattr(model_to_filter, k)==v if v!='null' else getattr(model_to_filter, k)==None for k,v in ex_filters.items()])
            filters.extend([
                getattr(model_to_filter, k) >= str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='gte'
                else getattr(model_to_filter, k) <= str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='lte'
                else getattr(model_to_filter, k) > str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='gt'
                else getattr(model_to_filter, k) < str_to_datetime(val.split(":", 1)[1]) if val.split(":", 1)[0]=='lt'
                else getattr(model_to_filter, k) == str_to_datetime(val)
                for k,v in dte_filters.items() for val in v 
            ])

            base = base.filter(*filters)

            if params['sort']:
                sort = [getattr(model_to_filter, key[1:]).desc() if re.search(SORT_STR_X, key) else getattr(model_to_filter, key).asc()for key in params['sort']]
                base = base.order_by(*sort)
            
            if params['q']:
                q_or, fts = [], []
                [ q_or.append(item) if re.search(Q_STR_X, item) else fts.append(item) for item in params['q'] ]
                q_or = or_(*[getattr(model_to_filter, q.split(':')[0]).match(q.split(':')[1]) if q.split(':')[1]!='null' else getattr(model_to_filter, q.split(':')[0])==None for q in q_or])
                fts = or_(*[getattr(model_to_filter, col[0]).ilike(f'%{val}%') for col in model_to_filter.c() if col[1]==str for val in fts])
                
                base = base.filter(fts).filter(q_or)
            data = base.offset(params['offset']).limit(params['limit']).all()
            return {'bk_size':base.count(), 'pg_size':data.__len__(), 'data':data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))
            
    async def update(self, id, payload, db:Session, images=None):
        try:
            rows = db.query(self.model).filter(self.model.id==id).update(schema_to_model(payload, True), synchronize_session="fetch")
            db.commit()
            return await self.read_by_id(id, db)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
        except MaxOccurrenceError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except AssertionError as e:
            raise HTTPException(status_code=400, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))

    async def delete(self, id, db:Session, filter_key:str=None):
        try:
            rows=db.query(self.model).filter(self.model.id==id).delete(synchronize_session=False)
            db.commit()
            return f"{rows} row(s) deleted"
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))

    async def bk_create(self, payload, db:Session):
        try:
            if db.bind.dialect.name=='sqlite':
                db.add_all([self.model(**payload.dict()) for payload in payload])
                db.commit()
            else:
                rows = db.execute(self.model.__table__.insert().returning(self.model).values([payload.dict() for payload in payload]))
                db.commit()
                return rows.fetchall()
        except Exception as e:
            code = 400 if isinstance(e, AssertionError) else 409 if any((
                isinstance(e, IntegrityError),
                isinstance(e, MaxOccurrenceError)
            )) else 500
            raise HTTPException(status_code=code, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))

    async def bk_update(self, payload, db:Session, **kwargs):
        try:
            _and, _or = kwargs.get("and", {}), kwargs.get("or", {}) 
            rows = db.query(self.model).filter_by(
                and_(**_and), 
                or_(**_or)
            ).update(payload.dict(exclude_unset=True), synchronize_session="fetch")
            db.commit()
            # session.query(Users).filter(Users.id.in_(subquery....)).delete(synchronize_session=False)
            return 'success', {"info":f"{rows} row(s) updated"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))

        # stmt = update(User).where(User.name == "squidward").values(name="spongebob").execution_options(synchronize_session="fetch")
        # result = session.execute(stmt) # The result object returned is an instance of CursorResult;

    async def bk_delete(self, ids:list, db:Session, use_field:str=None, **kwargs):
        try:
            subq = getattr(self.model, use_field).in_(ids) if use_field else self.model.id.in_(ids)
            rows = db.query(self.model).filter(subq).filter_by(**kwargs).delete(synchronize_session=False)
            db.commit()
            return f"{rows} row(s) deleted"
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message().split('DETAIL:  ', 1)[1], type= e.__class__.__name__))
        except MaxOccurrenceError as e:
            raise HTTPException(status_code=409, detail=http_exception_detail(msg=e._message(), type= e.__class__.__name__))
        except Exception as e:
            raise HTTPException(status_code=500, detail=http_exception_detail(msg=f"{e}", type= e.__class__.__name__))

    def get_related_model(self, related_name:str):
        relation = getattr(self.model, related_name)
        if not isinstance(relation.prop, RelationshipProperty):
            raise AttributeError(f"{related_name} is not a valid relation")
        return relation, relation.prop.mapper.class_

    def _base(self, db:Session, fields=None, related_name:str=None, resource_id:int=None):  
        if related_name and resource_id:
            relation, related_model = self.get_related_model(related_name)
            b_fields = [getattr(related_model, field.strip()) for field in fields] if fields!=None else [related_model]  
            base = db.query(*b_fields).join(related_model, relation).filter(self.model.id==resource_id)
            model = related_model
        else:
            b_fields = [getattr(self.model, field.strip()) for field in fields]  if fields!=None else [self.model] 
            base = db.query(*b_fields)
            model = self.model
        return model, base
        
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
            Parameter('fields', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex=f'({q_str})$')),
            Parameter('q', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex=Q_X.format(cols=f'({q_str})') if q_str else '^[\w]+$|^[\w]+:[\w]+$')),
            Parameter('sort', Parameter.KEYWORD_ONLY, annotation=List[str], default=Query(None, regex=sort_str if sort_str else '(^-)?\w')),]) 
        if self._actions:
            params.extend([Parameter('action', Parameter.KEYWORD_ONLY, annotation=str, default=Query(None))])
        wrapper.__signature__ = Signature(params)
        return wrapper

class Upload:
    def __init__(self, file, upload_to, size=None):
        self.file = file
        self.upload_to = upload_to
        self.size = size

    def _ext(self):
        return pathlib.Path(self.file.filename).suffix

    def file_allowed(self, ext=None):
        ext=ext if ext else self._ext()
        if ext in cfg.UPLOAD_EXTENSIONS["IMAGE"]:
            return True, "images/"
        elif ext in cfg.UPLOAD_EXTENSIONS["AUDIO"]:
            return True, "audio/"
        elif ext in cfg.UPLOAD_EXTENSIONS["VIDEO"]:
            return True, "videos/"
        elif ext in cfg.UPLOAD_EXTENSIONS["DOCUMENT"]:
            return True, "documents/"
        raise UploadNotAllowed('Unsupported file extension')
    
    def _path(self):
        _, url = self.file_allowed()

        tmp_path = os.path.join(cfg.UPLOAD_ROOT, url)

        path = os.path.join(tmp_path, f'{self.upload_to}')
                
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
        
    def _url(self):
        name, cnt = "_".join(os.path.splitext(self.file.filename)[0].split()), 1
        url = os.path.join(self._path(), f'{name}{self._ext()}')
        while pathlib.Path(url).exists():
            filename = f"{name}_{cnt}{self._ext()}"
            url = os.path.join(self._path(), f'{filename}')
            cnt+=1
        return url
    
    def path(self):
        self._path()

    def _image(self):
        url = self._url()
        try:
            with Image.open(BytesIO(self.file.file.read())) as im:
                im.thumbnail(self.size if self.size else im.size)
                im.save(url)
        finally:
            self.file.file.close()
            return url

    def _save_file(self):
        url = self._url()
        try:
            with open(url, "wb") as buffer:
                shutil.copyfileobj(self.file.file, buffer)
        finally:
            self.file.file.close()
            return url

    def save(self, *args, **kwargs):
        if cfg.settings.USE_S3:
            url = '/'+os.path.relpath(self._url(), cfg.BASE_DIR) 
            s3_upload(self.file, object_name=url) # push to celery to upload
        else:
            if self.file:
                url = self._image() if self.file.content_type.split("/")[0]=="image" else self._save_file()
                url = '/media/'+os.path.relpath(url,  cfg.UPLOAD_ROOT) 
            else:
                url = None
        return f"S3:{url}" if cfg.settings.USE_S3 else f"LD:{url}" if url else None

class FileReader:
    def __init__(self, file, header, supported_extensions:list=[]):
        self.file=file
        self.header = header
        self._supported_ext = SUPPORTED_EXT
        self._supported_ext.extend(supported_extensions)
        self._supported_ext = list(set(self._supported_ext))

    def _ext(self):
        return pathlib.Path(self.file.filename).suffix

    def _csv(self, to_dict:bool=True, replace_nan_with=None):
        df = pd.read_csv(self.file.file, usecols=self.header)[self.header]
        return self.validate_rows(df, to_dict, replace_nan_with=replace_nan_with)
       
    def _excel(self, to_dict:bool=True, replace_nan_with=None):
        df = pd.read_excel(self.file.file, usecols=self.header)[self.header]
        return self.validate_rows(df, to_dict, replace_nan_with=replace_nan_with)
    
    def verify_ext(self):
        return self._ext() in self._supported_ext

    def validate_rows(self, df, to_dict:bool=True, replace_nan_with=None):
        if to_dict:
            return [{k:None if pd.isna(v) else v for (k,v) in row.items()} for row in df.to_dict(orient="records")] if not replace_nan_with else df.fillna(replace_nan_with).to_dict(orient="records")
        return [[None if pd.isna(item) else item for item in row] for row in np.array(df[self.header].drop_duplicates())] if not replace_nan_with else np.array(df[self.header].fillna(replace_nan_with).drop_duplicates())

    async def read(self, to_dict:bool=True, replace_nan_with=None):
        try:
            if not self.verify_ext():
                raise FileNotSupported('file extension not supported')
            if self._ext() in [".csv",".CSV"]:
                rows = self._csv(to_dict=to_dict, replace_nan_with=replace_nan_with)
            else:
                rows = self._excel(to_dict=to_dict, replace_nan_with=replace_nan_with)
            return rows
        finally:
            await self.file.close()