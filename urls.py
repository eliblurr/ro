from main import app

@app.get('/')
async def root():
    return 'Restaurant Order Link'

from routers.location.main import router as location

app.include_router(location, tags=['Location'])
