from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import logging, aiohttp_jinja2, jinja2
from app.routes import setup_routes
from config import SECRET_KEY
import base64
from hashlib import sha256

class WebServer:
    def __init__(self, app):
        self.app = app
        setup(self.app, EncryptedCookieStorage("h938tKugDeZ0LJvr57NhuO93xojalD2xh4ptSFE8cHI="))

        aiohttp_jinja2.setup(
            self.app,
            loader=jinja2.FileSystemLoader('src/templates'),
            enable_async=True
        )

        setup_routes(self.app)
        self.runner = None

    async def start(self, host='localhost', port=8080):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, host, port)
        await site.start()
        logging.info(f'Server started at http://{host}:{port}')

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()
