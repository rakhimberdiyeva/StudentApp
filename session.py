from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://postgres:111@localhost:5432/StudentApp")

async_session = async_sessionmaker(engine, expire_on_commit=False)