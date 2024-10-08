from fastapi import FastAPI
from .database import engine
from .models import Base

app = FastAPI()

async def startup():
    # Асинхронное создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# В старте приложения
@app.on_event("startup")
async def on_startup():
    await startup()


