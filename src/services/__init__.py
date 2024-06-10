from services.wpp_client.wpp_api_client import WPPApiClient
from services.wpp_client.wpp_socket_client import WPPSocketClient
from services.wpp_client.session import WPPSession
from services.database.database_client import DatabaseClient
from services.web_server import WebServer
from aiohttp import web
import asyncio


class Services:
    def __init__(self):
        self. wppApiClient=WPPApiClient()
        self. wppSocketClient=WPPSocketClient()
        self.wppSession=WPPSession()

        self.webApp = web.Application()
        self.webServer=WebServer(self.webApp)

        self.dbClient = DatabaseClient()

    async def start(self, manager) -> None:
        self.webApp["manager"] = manager

        #start database
        await self.dbClient.start()
        #start wppSockeClient
        await self.wppSocketClient.start()

        self.web_server_task = asyncio.create_task(self.webServer.start())
        self.wpp_socket_client_task = asyncio.create_task(self.wppSocketClient.listen())

        await self.wppSession.start(self)
