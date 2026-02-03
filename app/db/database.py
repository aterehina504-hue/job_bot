from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is not set")

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
