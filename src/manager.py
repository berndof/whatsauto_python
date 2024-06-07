import logging, asyncio, aiofiles, os
from config import TOKEN_FILE_PATH, SESSION_NAME, ENV, DEV_PHONE, SECRET_KEY
import services
import bot
from aiohttp import web
import models
from aiohttp import web
import bcrypt


class Manager(object):

    def __init__(self) -> None:
        #* temporario
        self.security = self.Security(self)
        self.admin = self.Admin(self)
        ####

        self.wppApiClient = services.WPPApiClient()
        self.wppSocketClient = services.WPPSocketClient()

        self.app = web.Application()
        self.app["manager"] = self

        self.webServer = services.WebServer(self.app)
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

        #*test
        await self.admin.create_superuser("admin", "admin")

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

    class Security(object):

        def __init__(self, manager) -> None:
            self.manager = manager

        def get_password_hash(self, password):
            logging.debug("hashing password")
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password

        def check_password(self, password, hashed_password):
            logging.debug("checking password")
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)  # pass the bytes object directly

        async def authenticate(self, username, password):
            user = await models.User.get_or_none(username=username)
            if not user:
                return None
            if not self.check_password(password, user.password):
                return None
            return user

    class Admin(object):
        def __init__(self, manager):
            self.manager = manager

        async def create_superuser(self, username, password):
            password_hash = self.manager.security.get_password_hash(password)
            print(password_hash)
            user = await models.User.get_or_none(username=username)
            if not user:
                logging.debug("creating superuser")
                await models.User.create(username=username, password=password_hash, is_admin=True)
            return user
