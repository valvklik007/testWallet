from fastapi import FastAPI
from . import views
from .database import engine, Base

app = FastAPI(title='API v1 Кошелек')

app.include_router(views.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


