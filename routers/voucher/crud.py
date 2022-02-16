from sqlalchemy.orm import Session
from database import SessionLocal
from schedulers import scheduler
from . import models, schemas
from cls import CRUD

voucher = CRUD(models.Voucher)

def expire_voucher(pk, db:Session=SessionLocal()):
    voucher = db.query(models.Voucher).get(pk)
    if voucher:
        voucher.status="expired"
        db.commit()
    return True

def schedule_expiry(pk, expiry):
    scheduler.add_job(
        expire_voucher,
        trigger='date',
        kwargs={'pk':pk},
        id=f'ID-VOUCHER-{pk}',
        replace_existing=True,
        run_date=expiry
    )
    return True