from typing import AsyncGenerator
from sqlalchemy import MetaData 
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from configs import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?async_fallback=True"

metadata = MetaData()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session