from sqlalchemy.orm import Session

class CRUD:
    def __init__(self, model):
        self.model=model

    async def create(self, payload, db:Session):
        obj = self.model(**payload.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj) 
        return obj  

    async def read_by_id(self, id, db:Session):
        return db.query(self.model).filter(self.model.id==id).first()

    async def read(self, db:Session, search:str=None, value:str=None, skip:int=0, limit:int=100):
        base = db.query(self.model)
        if search and value:
            try:
                base = base.filter(self.model.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                pass
        return base.offset(skip).limit(limit).all()

    async def update(self, id, payload, db:Session):
        db.query(self.model).filter(self.model.id==id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await self.read_by_id(id, db)

    async def delete(self, id, db:Session):
        rows = db.query(self.model).filter(self.model.id==id).delete()
        db.commit()
        return rows