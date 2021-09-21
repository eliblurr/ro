from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import settings

'''
    current version of sqlalchemy does not support [postgres]:// 
    hence change to postgresql to accomodate
'''

db_url = 'postgresql:'+settings.DATABASE_URL.split(':', 1)[1]

# postgresql://postgres:postgres@0.0.0.0:8888/ro4
# postgresql://postgres:postgres@0.0.0.0:8888/ro4

# print(settings.DATABASE_URL.split(':', 1))

# postgres://postgres:postgres@0.0.0.0:8888/ro4
# engine = create_engine(settings.DATABASE_URL)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

'''
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, ForeignKey
@app.middleware("http")
async def session(request:Request, call_next):
    db = SessionLocal(tenant_id=request.headers.get('tenant', None))
    try:
        db.tenant = request.headers.get('tenant', None)
        request.state.db = db
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db(request:Request):
    return request.state.db

class Base(object):
    __multitenant__ = True

    @declared_attr
    def restaurant_id(cls):
        if not cls.__multitenant__:
            return None
        return Column(Integer, ForeignKey("restaurants.id"), index=True)

# Base = declarative_base(cls=Base)
class TenantSession(session.Session):
    def __init__(self, *args, **kwargs):
        self.tenant = self.verify_tenant(self.tenant)
        super(TenantSession, self).__init__(*args, **kwargs)

    def query(self, *args, **kwargs):
        print(
            str(
                super(
                    TenantSession, self).query(*args, **kwargs
                )
            )
        )
        return super(TenantSession, self).query(*args, **kwargs)

    def add(self, instance, *args, **kwargs):
        self.check_instance(instance)
        instance.tenant_id = self.tenant.id
        super(TenantSession, self).add(instance, *args, **kwargs)

    def delete(self, instance, *args, **kwargs):
        self.check_instance(instance)
        super(TenantSession, self).delete(instance, *args, **kwargs)

    def merge(self, instance, *args, **kwargs):
        self.check_instance(instance)
        super(TenantSession, self).merge(instance, *args, **kwargs)

    def verify_tenant(self):
        tenant = self.query(models.Tenant, safe=False).first()
        return tenant

    def check_instance(self, instance):
        if instance.__multitenant__ and self.tenant is None:
            raise UnboundTenantError("Tried to do a tenant-safe operation in a tenantless context.")

        if instance.__multitenant__ and instance.tenant_id is not None and instance.tenant_id != self.tenant.id:
            raise TenantConflict(("Tried to use a %r with tenant_id %r in a session with " +"tenant_id %r") % (type(instance), instance.tenant_id, self.tenant.id))

def SessionLocal(tenant_id=None):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    if tenant_id:
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=TenantSession)
    return Session()
'''