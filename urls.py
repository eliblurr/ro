from starlette.responses import RedirectResponse
from main import app

@app.get('/')
async def root():
    return RedirectResponse(url='/redoc')

@app.get('/resource/')
@app.get('/resource/{rec_id}')
async def root(rec_id:int=None):
    if rec_id:
        return rec_id
    return 

from routers.location.main import router as location

app.include_router(location, tags=['Location'])
