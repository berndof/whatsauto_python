from fastapi import FastAPI
import asyncio
from modules.manager import Manager

class FastAPIServer:
    def __init__(self, manager:Manager, host:str="0.0.0.0", port:int=8000):
        self.manager = manager
        self.host = host
        self.port = port
        self.app = FastAPI()
    
    async def start(self):
        await self._setup_routes()
        asyncio.create_task(self.run(self.host, self.port))
        
    async def _setup_routes(self):
        @self.app.post("/start-session")
        async def start_session():
            status, qr_data = await self.manager.start_session()
            return {
                "qr_data":qr_data,
                "session_status": status,
            }

    async def run(self, host:str, port:int):
        
        import uvicorn
        config = uvicorn.Config(self.app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()