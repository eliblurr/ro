import config as cfg, utils, os
from . import models, schemas
from pathlib import Path
from cls import CRUD

async def create(files, payload, db):
    db.add_all(
        [ models.Image(
            detail =  f"{cfg.IMAGE_URL}{utils.create_image(file_b, cfg.IMAGE_ROOT)}", 
            small = f"{cfg.IMAGE_URL}{utils.create_image(file_b, cfg.IMAGE_ROOT, cfg.SMALL)}",
            listquad = f"{cfg.IMAGE_URL}{utils.create_image(file_b, cfg.IMAGE_ROOT, cfg.LISTQUAD)}",
            thumbnail = f"{cfg.IMAGE_URL}{utils.create_image(file_b, cfg.IMAGE_ROOT, cfg.THUMBNAIL)}", 
            **payload.dict()
        ) for file_b in [file.file.read() for file in files]]
    )
    db.commit()
    return {"data":"success"}
    
async def delete(id, db):
    obj = models.Image.query.filter_by(id=id).one()
    db.delete(obj)
    # os.remove(f'{cfg.IMAGE_ROOT}/{Path(obj.name).resolve().name}')
    # db.commit()
    return {"data":"success"}
