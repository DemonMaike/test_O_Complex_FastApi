from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import user, db


app = FastAPI()
app.mount('/static', StaticFiles(directory='static/'), name='static')

app.include_router(user.router, tags=['user'])
app.include_router(db.router, tags=['db'])