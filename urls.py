from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from starlette.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from main import app
import config as cfg

from routers.ad.main import router as ad
from routers.faq.main import router as faq
from routers.meal.main import router as meal
from routers.table.main import router as table
from routers.media.main import router as media
from routers.order.main import router as order
from routers.policy.main import router as policy
from routers.voucher.main import router as voucher
from routers.location.main import router as location
from routers.currency.main import router as currency
from routers.category.main import router as category
from routers.restaurant.main import router as restaurant

app.include_router(location, tags=['Locations'])
app.include_router(ad, tags=['Adverts'], prefix='/ads')
app.include_router(meal, tags=['Meals'], prefix='/meals')
app.include_router(order, tags=['Orders'], prefix='/orders')
app.include_router(table, tags=['Tables'], prefix='/tables')
app.include_router(media, tags=['Media'], prefix='/uploads')
app.include_router(policy, tags=['Policies'], prefix='/policies')
app.include_router(voucher, tags=['Vouchers'], prefix='/vouchers')
app.include_router(currency, tags=['Currencies'], prefix='/currencies')
app.include_router(category, tags=['Categories'], prefix='/categories')
app.include_router(restaurant, tags=['Restaurant'], prefix='/restaurants')
app.include_router(faq, tags=['Frequently Asked Questions'], prefix='/frequently-asked-questions')

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,)

@app.get('/', name='Home', tags=['Docs'], include_in_schema=False)
async def redoc_html():
    def custom_openapi():
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description="API documentation for food ordering service in restaurants \n\n <a href='/docs' style='color:hotpink;cursor:help'>Interactive Swagger docs</a>",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": f"{cfg.STATIC_URL}/images/logo.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    app.openapi = custom_openapi
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/js/redoc.standalone.js",
        redoc_favicon_url=f"{cfg.STATIC_URL}/images/logo.png"
    )

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    def custom_openapi():
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description="API documentation for food ordering service in restaurants \n\n <a href='/' style='color:hotpink;cursor:help'>see official API docs</a>",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": f"{cfg.STATIC_URL}/images/logo.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    app.openapi = custom_openapi
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url=f"{cfg.STATIC_URL}/images/logo.png",
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )

from pydantic import BaseModel
from typing import List, Optional
from routers.currency.models import Currency
from utils import schema_to_model, http_exception_detail
from fastapi import HTTPException

class Z(BaseModel):
    symbol: str

    class Meta:
        model = Currency

class A(BaseModel):
    symbol: str
    title: List[Z]

    class Meta:
        model = Currency

class B(BaseModel):
    symbol: Optional[str]
    title: A

    class Meta:
        model = Currency

@app.post("/test")
async def test(payload:B):
    try:
        return schema_to_model(payload, exclude_unset=True)
    except AttributeError as e:
        raise HTTPException(status_code=500, detail= http_exception_detail(loc=('string'), msg=e.__str__(), type=f"{e.__class__.__name__}"))

from fastapi import Form

class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

print(Form.__annotations__)

@app.post("/test")
async def test():
    pass