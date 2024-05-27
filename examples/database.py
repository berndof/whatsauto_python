from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DatabaseClient:
    def __init__(self, environment, DB_HOST=None, DB_PORT=None, DB_USER=None, DB_PASSWORD=None, DB_NAME=None):
        if environment == "dev" or not environment:
            self.engine = create_async_engine("sqlite+aiosqlite:///db.sqlite")
        elif environment == "prod":
            self.engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        else:
            raise ValueError("Invalid environment")

        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_all_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def add(self, obj):
        async with self.Session() as session:
            async with session.begin():
                session.add(obj)

    async def get(self, model, **kwargs):
        async with self.Session() as session:
            return await session.scalars(session.query(model).filter_by(**kwargs)).first()

    async def get_all(self, model, **kwargs):
        async with self.Session() as session:
            return await session.scalars(session.query(model).filter_by(**kwargs)).all()

    async def update(self, obj):
        async with self.Session() as session:
            async with session.begin():
                session.add(obj)

    async def delete(self, obj):
        async with self.Session() as session:
            async with session.begin():
                await session.delete(obj)'' 2'