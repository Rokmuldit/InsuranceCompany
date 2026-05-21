from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from database import get_async_session, init_db
from contextlib import asynccontextmanager

from routers import paid_plans, insurance_contracts, insurance_events, insurance_payments, personal_data, client, agent

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    await init_db()
    yield

app = FastAPI(title="Insurance Company API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(text("SELECT 'Welcome to the Insurance Company API on MSSQL' AS message"))
    row = result.fetchone()
    return {"message": row.message if row else "Error"}

@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

app.include_router(paid_plans.router)
app.include_router(insurance_contracts.router)
app.include_router(insurance_events.router)
app.include_router(insurance_payments.router)
app.include_router(personal_data.router)
app.include_router(client.router)
app.include_router(agent.router)