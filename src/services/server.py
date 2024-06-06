from aiohttp import web
import asyncio

class WebServer:
    def __init__(self, manager):
        self.app = web.Application()
        self.app.router.add_get('/admin', self.index)
        self.runner = None
        self.manager = manager

    async def index(self, request):
        print("hello")
        return web.Response(text="<html><body>Hello, world</body></html>", content_type='text/html')

    async def start(self, host='localhost', port=8080):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, host, port)
        await site.start()
        #print(f'Server started at http://{host}:{port}')

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()
