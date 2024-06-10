import logging, asyncio, aiofiles, os
from config import TOKEN_FILE_PATH, SESSION_NAME, ENV, DEV_PHONE, SECRET_KEY, BOT_PHONE
from services import Services
from bot import Bot
from aiohttp import web
from app.modules.admin import Admin
import models


class Manager(object):

    def __init__(self) -> None:

        self.services = Services()
        self.bot = Bot(self.services)

    async def start(self) -> None:
        await self.services.start(self)

        #?Test##
        await self._createTestQueues()
        await Admin.create_superuser("admin", "admin")



        ########

        await self.bot.startListenMessages()


    async def _createTestQueues(self):
        queues = {
            1: ("queue1", "Bem vindo ao queue 1"),
            2: ("queue2", "Bem vindo ao queue 2"),
            3: ("queue3", "Bem vindo ao queue 3")
        }

        for index, (name, greetings_message) in queues.items():
            await models.Queue.get_or_create(name=name, greetings_message=greetings_message, index=index)

    """ async def _get_my_chat(self):
        await self.bot.sendMessage("discovering my chat", phone=BOT_PHONE)
        #if chat doesnt exists in wpp, returns false
        endpoint = f"{self.services.wppSession.name}/chat-by-id/{BOT_PHONE}"

        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {self.services.wppSession.token}',
            'Content-Type': 'application/json'
        }

        response = await self.services.wppApiClient.makeRequest("GET", endpoint, headers)
        chat_phone = response["id"]["user"]
        chat, exists = await models.Chat.get_or_create(phone=int(chat_phone), name="MY_CHAT")
        return chat """

    async def close(self) -> None:
        await self.db_client.close()
        #await self.fastapi_server.close()
        await self.wpp_socket_client.close()
        await self.wpp_api_client.close()#

        loop = asyncio.get_event_loop()
        loop.stop()


