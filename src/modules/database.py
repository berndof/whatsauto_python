import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from modules import models


class DatabaseClient:
    def __init__(self, environment, DB_HOST=None, DB_PORT=None, DB_USER=None, DB_PASSWORD=None, DB_NAME=None) -> None:
        self.engine = create_async_engine(
            self._construct_db_url(environment, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME),
            echo=True,  # You can set this to False to reduce logging
        )
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def _construct_db_url(self, environment, DB_HOST, DB_PORT, DB_user, DB_PASSWORD, DB_NAME) -> str:
        if environment == "dev" or not environment:
            return "sqlite+aiosqlite:///db.sqlite"
        elif environment == "prod":
            return f"postgresql+asyncpg://{DB_user}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:
            raise ValueError("Invalid environment")

    async def create_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

    async def get_db_session(self) -> Session:
        # Each call to get_session will provide a new session
        return self.Session()

    async def insert_whatsapp_session(self, whatsapp_session:models.WhatsappSession) -> models.WhatsappSession | None:
        async with (await self.get_db_session()) as session:
            try:
                session.add(whatsapp_session)
                await session.commit()
                return whatsapp_session
            except IntegrityError:
                print("WhatsappSession already exists")
                #TODO add logging
                await session.rollback()

    # Placeholder for migration handling
    async def run_migrations(self):
        pass

    # Placeholder for error handling
    async def handle_errors(self):
        pass