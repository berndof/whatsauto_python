from fastapi import FastAPI
from config import FASTAPI_HOST, FASTAPI_PORT
import asyncio

class FastAPIServer(object):
    def __init__(self, manager):
        self.manager = manager
        self.app = FastAPI()
    
    async def start(self):
        await self.__setup_routes()
        asyncio.create_task(self.run())
        
    async def __setup_routes(self):
        
        @self.app.post("/start-session")
        async def start_session():
            status, qr_data = await self.manager.start_session()
            return {
                "qr_data":qr_data,
                "session_status": status,
            }

    async def run(self):
        import uvicorn
        config = uvicorn.Config(self.app, host=FASTAPI_HOST, port=FASTAPI_PORT, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()