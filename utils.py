from config import JWT_ALGORITHM, settings
from datetime import timedelta, datetime
from math import ceil, floor, log2
from typing import Optional
import inspect, secrets, os
from fastapi import Form
import sqlalchemy as sa
from io import BytesIO
from PIL import Image

def to_tsvector(lang='pg_catalog.english', *columns):
    s = " || ' ' || ".join(columns)
    return sa.sql.func.to_tsvector(lang, sa.text(s))

def as_form(cls):
    form = [
        inspect.Parameter( model_field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=Form(model_field.default) if not model_field.required else Form(...),
            annotation=model_field.outer_type_
        ) for _ ,model_field  in cls.__fields__.items()
    ]
    def _cls_(**data):
        return cls(**data)
    _cls_.__signature__ = inspect.signature(_cls_).replace(parameters=form)
    setattr(cls, 'as_form', _cls_)
    return cls

def gen_code(nbytes=8):
    return secrets.token_urlsafe(nbytes)

def convert_image(image, directory, ext="jpg"):
    with Image.open(BytesIO(image.file.read())) as im:
        name = f"{gen_code()}"
        path = f"{directory}/{name}.{ext}"
        im.save(path)
        return name

def create_image(image, directory, size=None):
    with Image.open(BytesIO(image)) as im:
        name = f"{gen_code()}.jpg"
        path = f"{directory}/{name}"
        im.thumbnail(size if size else im.size)
        im.save(path)
        return name

def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"

def schema_to_model(schema, exclude_unset=False):
    """Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.model."""
    parsed_schema = dict(schema)
    try:
        for k,v in parsed_schema.items():
            if isinstance(v, list) and len(v) and is_pydantic(v[0]):
                parsed_schema[k] = [item.Meta.model(**schema_to_model(item)) for item in v]
            elif is_pydantic(v):
                parsed_schema[k] = v.Meta.model(**schema_to_model(v))
    except AttributeError:
        raise AttributeError(f"found nested pydantic model in {schema.__class__} but Meta.model was not specified.")
    
    if exclude_unset:
        parsed_schema = {k: v for k, v in parsed_schema.items() if v is not None}
    
    return parsed_schema

def http_exception_detail(loc=None, msg=None, type=None):
    detail = {}
    if loc:
        detail.update({"loc":loc if loc.__class__ in [list, set, tuple] else [loc]})
    if msg:
        detail.update({"msg":msg})
    if msg:
        detail.update({"type":type})
    return [detail]

def type_2_pow(n):
    assert ceil(log2(n)) == floor(log2(n)), f'{n} is not a power 2'
    return n

def list_sum(ls):
    return sum(ls)

def create_jwt(data:dict, expires_delta:Optional[timedelta]=None):
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=settings.ACCESS_SESSION_DURATION_IN_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt(jwt:str):
    return jwt.decode(data, settings.SECRET_KEY, settings.ALGORITHM)

def str_to_datetime(string, frmt='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(string, frmt)