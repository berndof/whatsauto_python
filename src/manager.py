import logging, asyncio, aiofiles, os
from config import TOKEN_FILE_PATH, SESSION_NAME, ENV, DEV_PHONE, SECRET_KEY
import services
import bot
import app


class Manager(object):

    def __init__(self) -> None:

        self.wppApiClient = services.WPPApiClient()
        self.wppSocketClient = services.WPPSocketClient()
        self.webServer = services.WebServer()
        self.db = services.DatabaseClient()

        from services.session import WPPSession
        self.session = WPPSession(self)

        self.bot = bot.app(self)

    async def start(self) -> None:

        await self.db.start()
        await self.wppSocketClient.start()

        self.web_server_task = asyncio.create_task(self.webServer.start())
        self.wpp_socket_client_task = asyncio.create_task(self.wppSocketClient.listen())

        await self.session.start()
        await self.bot.startListenMessages()

    async def sendMessage(self, chat, message):
        endpoint = f"{self.session.name}/send-message"

        if ENV == "dev" and chat.phone != DEV_PHONE:
            logging.debug(f"ignoring message from {chat.phone} because it is not dev phone")
            return

        body = {
            "phone": f"{chat.phone}",
            "message": f"{message}"
        }

        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {self.session.token}',
            'Content-Type': 'application/json'
        }
        return await self.wpp_api_client.makeRequest("POST", endpoint, headers, body)

    async def close(self) -> None:
        await self.db_client.close()
        #await self.fastapi_server.close()
        await self.wpp_socket_client.close()
        await self.wpp_api_client.close()#

        loop = asyncio.get_event_loop()
        loop.stop()