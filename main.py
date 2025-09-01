from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   
    yield

app = FastAPI(title="Digital Wallet", lifespan=lifespan)

app.include_router(router)  
