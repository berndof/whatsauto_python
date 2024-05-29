""" 
@app.post()
@app.put()
@app.delete()
@app.options()
@app.head()
@app.patch()
@app.trace()a
"""
from fastapi import FastAPI
import asyncio
import logging

class FastAPIServer:
    def __init__(self, manager):
        self.manager = manager
        self.app = FastAPI()
    
    async def start(self, host:str="0.0.0.0", port:int=8000):
        await self._setup_routes()
        asyncio.create_task(self.run(host, port))

    async def _setup_routes(self):
        
        @self.app.post("/generate-token")
        async def generate_token():
            token = await self.manager.generate_token()
            return {"token": token}

    async def run(self, host:str, port:int):
        import uvicorn
        config = uvicorn.Config(self.app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
