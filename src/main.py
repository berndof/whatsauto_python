import asyncio
from modules.manager import Manager
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")

api_host = "http://localhost:21465/api"
secret_key = "Sccdev76"
session_name = "dev"
environment = "dev"
fastapi_port = "8000"
fastapi_host = "0.0.0.0"

manager = Manager(api_host, secret_key, session_name) 
#PASSAR O BOT AQUI

async def main():
    
    await manager.start(environment) #set db, start the consumer ...
    await manager.socket_client.start() #socketio client
    await manager.api_server.start()
            

    # Keep the event loop running 
    # TODO i think this loop can be replaced for some async loop function
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())