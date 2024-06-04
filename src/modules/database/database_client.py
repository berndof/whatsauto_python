import logging
from tortoise import Tortoise
from modules.config import DATABASE_URL
from modules import models

class DatabaseClient(object):

    async def start(self):
        await Tortoise.init(
            db_url = DATABASE_URL,
            modules = {"models": ["modules.models"]}
        )
        logging.info('database started')
    
        await Tortoise.generate_schemas()
        logging.debug('database generated schemas')
        
    async def close(self):
        await Tortoise.close_connections()

