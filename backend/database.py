from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import settings

# For MSSQL with aioodbc, the URL format is:
# mssql+aioodbc://<username>:<password>@<host>:<port>/<database>?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no...
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True,
    # MSSQL specific: some drivers might need pool_pre_ping
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def init_db():
    master_engine = create_async_engine(settings.MASTER_DB, isolation_level="AUTOCOMMIT")

    async with master_engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sys.databases WHERE name = 'insurance_db'"))
        if not result.scalar():
            await conn.execute(text("CREATE DATABASE insurance_db"))

    await master_engine.dispose()

    with open('sql_scripts/SETUP/v1.sql', mode='r', encoding='utf-8') as f:
        sql_script = f.read()

    app_engine = create_async_engine(settings.ASYNC_DATABASE_URL)

    async with app_engine.begin() as conn:
        await conn.execute(text(sql_script))

    await app_engine.dispose()
