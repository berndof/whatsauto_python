import asyncio
from modules.manager import Manager
import uvicorn
from api_server import app
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")

api_host = "http://localhost:21465"
secret_key = "Sccdev76"
session_name = "dev"
environment = "dev"

config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
server = uvicorn.Server(config)

manager = Manager(api_host, secret_key, session_name) 
app.manager = manager

async def main():
    
    await manager.start(environment) #set db, start the consumer ...
    await manager.socket_client.start() #socketio client
    await server.serve() #fast_api
    
    # Keep the event loop running 
    # TODO i think this loop can be replaced for some async loop function
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())