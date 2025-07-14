from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.base import Base
from src.product.models import Product

DATABASE_URL = "postgresql+asyncpg://admin:admin123@postgres:5432/mydb"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)