from fastapi import Form
import sqlalchemy as sa
import inspect

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

