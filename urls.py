from starlette.responses import RedirectResponse
from main import app

from routers.faq.main import router as faq
from routers.policy.main import router as policy
from routers.location.main import router as location
from routers.currency.main import router as currency

app.include_router(location, tags=['Locations'])
app.include_router(policy, tags=['Policies'], prefix='/policies')
app.include_router(currency, tags=['Currencies'], prefix='/currencies')
app.include_router(faq, tags=['Frequently Asked Questions'], prefix='/frequently-asked-questions')

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,)

@app.get('/', name='Home', tags=['Docs'])
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/js/redoc.standalone.js",
    )

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()