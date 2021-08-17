from fastapi import Form
import sqlalchemy as sa
import inspect, secrets, os
from io import BytesIO
from PIL import Image

def to_tsvector_ix(lang, *columns):
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