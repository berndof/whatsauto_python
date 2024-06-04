# wpp_socket_client.py
import asyncio, socketio, logging
from modules.config import WPP_API_HOST

class WPPSocketIOClient(object):
    
    def __init__(self, manager) -> None:
        self.sio = socketio.AsyncClient()
        self.manager = manager

    async def connect(self) -> None:
        await self.sio.connect(WPP_API_HOST)
        logging.info("connecting to socket")

    async def listen(self) -> None:
        try:
            await self.sio.wait()
        except Exception as e:
            logging.error(f"{e} | While listening to event")

    async def on_connect(self):
        logging.info(f"socket connected on {WPP_API_HOST}")

    async def on_disconnect(self):
        logging.info(f"disconnected of socket on {WPP_API_HOST}")

    async def on_event(self, event, data):
        logging.debug(f"event recieved: {event}")
        #await self.manager.on_socket_event(event, data)
        print(self.manager.triggers)
        
        #TODO IMPROVE THIS
        for trigger in self.manager.triggers:
            if trigger.event_to_catch == str(event):
                logging.debug(f"trigger {trigger.name} set")
                await trigger.set(event, data)                    
                break

    async def start(self):
        await self.connect()

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("*", self.on_event)  # Listen to all events
        
        asyncio.create_task(self.listen())
