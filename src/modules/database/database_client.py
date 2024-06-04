import logging
from modules.config import engine, Base
from modules.database import dal

class DatabaseClient(object):
    def __init__(self):
        self.is_started = False
        self.access 
    
    async def create_all_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def start(self):    
        await self.create_all_tables()
        self.is_started = True
        
    async def get_one_chat(self, phone):
        async with engine.connect() as conn:
            result = await conn.execute(dal.ChatDAL.select().where(dal.ChatDAL.c.phone == phone))
            row = await result.fetchone()
            return row

