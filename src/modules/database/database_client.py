import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session

from modules.config import DATABASE_URL, engine, async_session, Base

class DatabaseClient(object):
    def __init__(self):
        self.is_started = False
    
    async def create_all_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def start(self):    
        await self.create_all_tables()
        self.is_started = True

    


        """async with async_session() as session:
            async with session.begin():
                chat_dal = ChatDAL(session)
                print("alo")
                return await chat_dal.create_chat("teste")"""