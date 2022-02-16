from . import models, schemas
from typing import List
from cls import CRUD

ad = CRUD(models.AD)
ad_locale = CRUD(models.ADLocale)

async def add_locale_to_ad(ad_id: int, locale_ids: List[int], db):
    payload = [schemas.ADLocale(ad_id=ad_id, locale_id=id)
               for id in locale_ids]
    return await ad_locale.bk_create(payload, db)

async def rem_locale_from_ad(ad_id: int, locale_ids: List[int], db):
    return await ad_locale.bk_delete(locale_ids, db, use_field='locale_id', ad_id=ad_id)