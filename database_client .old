
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
import logging

## REWORK ##
class DatabaseClient:
    def __init__(self, environment:str, config:dict) -> None:
        
        self.environment = environment
        self.engine = None
        self.Session = None
        self.config = config
    
    def __load_models(self):
        
        # rework, iterate inside all modules and load models from there
        # append models to list them return 
        
        from models.user import User
        
        return [User]

    async def start(self):
        
        if self.environment == "dev":
            url = "sqlite+aiosqlite:///./database.db"
        else: raise ValueError("invalid environment")
        
        self.engine = create_async_engine(url, echo=False)
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.__load_models()
        
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
        except ProgrammingError:
            await self.create_db()

    async def create_db(self):
        async with self.engine.begin() as conn:
            for model in self.models:
                await conn.run_sync(model.__table__.create)
                logging.debug(f"created table {model.__tablename__}")
                
    async def close(self):
        await self.engine.dispose()
    
    async def get_db_session(self):
        return self.Session()