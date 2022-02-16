from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from starlette.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from database import engine
from routers import *
from main import app
import config as cfg

app.include_router(auth, tags=['Authenticate'])
app.include_router(location, tags=['Locations'])
app.include_router(ad, tags=['Adverts'], prefix='/ads')
app.include_router(role, tags=['Roles'], prefix='/roles')
app.include_router(meal, tags=['Meals'], prefix='/meals')
app.include_router(menu, tags=['Menus'], prefix='/menus')
app.include_router(order, tags=['Orders'], prefix='/orders')
app.include_router(table, tags=['Tables'], prefix='/tables')
app.include_router(rating, tags=['Ratings'], prefix='/ratings')
app.include_router(policy, tags=['Policies'], prefix='/policies')
app.include_router(voucher, tags=['Vouchers'], prefix='/vouchers')
app.include_router(accounts, tags=['Accounts'], prefix='/accounts')
app.include_router(upload, tags=['Uploads'], prefix=f'{cfg.UPLOAD_URL}')
app.include_router(category, tags=['Categories'], prefix='/categories')
app.include_router(restaurant, tags=['Restaurant'], prefix='/restaurants')
app.include_router(faq, tags=['Frequently Asked Questions'], prefix='/frequently-asked-questions')

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,)

def get_custom_openapi(path='/redoc'):

    description = f"""
    API documentation for food ordering service in restaurants \n\n {
    "<a href='/docs' style='color:#c0392b;cursor:help'>Interactive Swagger docs</a>" if path=="/redoc" else 
    "<a href='/'>Official API docs</a>"
    }"""

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=description,
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": f"{cfg.STATIC_URL}/images/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    def custom_openapi():
        return get_custom_openapi(path='/docs')
    app.openapi = custom_openapi
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url=f"{cfg.STATIC_URL}/images/logo.png",
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )

@app.get('/', name='Home', tags=['Docs'], include_in_schema=False)
async def redoc_html():
    def custom_openapi():
        return get_custom_openapi(path='/redoc')
    app.openapi = custom_openapi
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/js/redoc.standalone.js",
        redoc_favicon_url=f"{cfg.STATIC_URL}/images/logo.png",
        with_google_fonts=True
    )

@app.post("/init", include_in_schema=False)
def init():  
    Base.metadata.create_all(bind=engine)

@app.delete("/terminate", include_in_schema=False)
def terminate():  
    Base.metadata.drop_all(bind=engine)
