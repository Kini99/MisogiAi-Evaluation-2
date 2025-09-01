
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routes import router
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Add dummy users if not present
        async with AsyncSession(engine) as session:
            from sqlalchemy import text
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            if count == 0:
                users = [
                    User(username="alice", email="alice@example.com", password="alice123", phone_number="1111111111", balance=100.0),
                    User(username="bob", email="bob@example.com", password="bob123", phone_number="2222222222", balance=150.0),
                    User(username="carol", email="carol@example.com", password="carol123", phone_number="3333333333", balance=200.0),
                ]
                session.add_all(users)
                await session.commit()
    yield

app = FastAPI(title="Digital Wallet", lifespan=lifespan)
app.include_router(router)
