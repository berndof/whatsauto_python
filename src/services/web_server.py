from aiohttp import web
import logging

class WebServer:
    def __init__(self):
        self.app = web.Application()
        self.app.router.add_get('/admin', self.index)
        self.runner = None

    async def index(self, request):
        print("hello")
        return web.Response(text="<html><body>Hello, world</body></html>", content_type='text/html')

    async def start(self, host='localhost', port=8080):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, host, port)
        await site.start()
        logging.info(f'Server started at http://{host}:{port}')

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()
