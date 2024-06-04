import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session


from modules.models import Base

class DatabaseClient(object):
    def __init__(self, environment:str, config:dict) -> None:
        
        if environment == 'dev':
            url = f'sqlite+aiosqlite:///sqlite.db'
        else:
            #TODO implement in future
            raise NotImplementedError("wrong environment")
        
        self.engine = create_async_engine(url, echo=config["echo"])
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        
        self.is_started = False
        
    async def create_all_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
    async def start(self):
        if not self.is_started:
            await self.create_all_tables()
            self.is_started = True
        else:
            raise NotImplementedError("DatabaseClient error")
    
        return self.is_started

    async def add_chat(self, chat):
        async with self.Session() as session:
            async with session.begin():
                session.add(chat)

