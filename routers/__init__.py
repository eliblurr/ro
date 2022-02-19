from routers.upload import *
from routers.user import *

from routers.location import *
from routers.rating import *
from routers.meal import *
from routers.table import *
from routers.menu import *
from routers.faq import * 
from routers.policy import *
from routers.category import *

from routers.voucher import *
from routers.order import *
from routers.restaurant import *
from routers.ad import *

from database import Base

__all__=[
    'Base',
    'role',
    'auth',
    'accounts',
    'location',
    'rating', 
    'meal',
    'table',
    'menu',
    'faq',
    'policy', 
    'category',
    'ad', 
    'voucher',
    'order', 
    'upload', 
    'restaurant',
]

from database import engine

# Base.metadata.create_all(bind=engine)
# print(Base.metadata.sorted_tables)
