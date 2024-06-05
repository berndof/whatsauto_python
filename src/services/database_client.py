import logging
from tortoise import Tortoise
from config import DATABASE_URL
import models
from typing import Any

class DatabaseClient(object):

    async def start(self):
        await Tortoise.init(
            db_url = DATABASE_URL,
            modules = {"models": ["models"]}
        )
        logging.info('database started')
    
        await Tortoise.generate_schemas()
        logging.debug('database generated schemas')
        
    async def close(self):
        await Tortoise.close_connections()

    async def getChatBy(self, property_name:Any, property_value:Any) -> models.Chat | None:
        if property_name not in models.Chat._meta.fields:
            logging.warn(f"property {property_name} doesnt exists Chat model ")
            raise ValueError(f"property {property_name} doesnt exists in Chat model")
        chat = await models.Chat.filter(**{property_name: property_value}).first()
        return chat if chat else None
    
    async def addChat(self, phone:str, name:str) -> models.Chat:
        chat = models.Chat(phone=phone, name=name)
        logging.debug(f"chat created: {chat}")
        await chat.save()
        return chat

    async def addQueue(self, name:str, greeting_message:str) -> models.Queue:
        queue = models.Queue(name=name, greetings_message=greeting_message)
        logging.debug(f"queue created: {queue}")
        await queue.save()
        return queue
    
    async def getQueues(self) -> list[models.Queue]:
        queues = await models.Queue.all()
        return queues
    
    async def getQueueBy(property_name:Any, property_value:Any) -> models.Queue | None:
        if property_name not in models.Queue._meta.fields:
            logging.warn(f"property {property_name} doesnt exists Queue model ")
            raise ValueError(f"property {property_name} doesnt exists in Queue model")
        queue = await models.Queue.filter(**{property_name: property_value}).first()
        return queue if queue else None