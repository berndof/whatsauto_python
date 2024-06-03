# wpp_socket_client.py
import asyncio
import socketio
import logging
from automations.triggers.socket_trigger import SocketTrigger, AsyncSocketTrigger

class WPPSocketIOClient:
    
    def __init__(self, url:str, manager) -> None:
        self.sio = socketio.AsyncClient()
        self.url = url
        self.manager = manager

    async def connect(self) -> None:
        await self.sio.connect(self.url)
        logging.info("connecting to socket")

    async def listen(self) -> None:
        try:
            await self.sio.wait()
        except Exception as e:
            logging.error(f"{e} | While listening to event")

    async def on_connect(self):
        logging.info(f"connected to socket on {self.url}")

    async def on_disconnect(self):
        logging.info(f"disconnected of socket on {self.url}")

    async def on_event(self, event, data):
        logging.debug(f"event recieved: {event}")
        #await self.manager.on_socket_event(event, data)
        print(self.manager.triggers)
        
        #TODO IMPROVE THIS
        for trigger in self.manager.triggers:
            logging.debug (f"checking trigger {trigger.name}")
            if trigger.event_to_catch == str(event):
                if type(trigger) == SocketTrigger:
                    trigger.set(event, data)
                if type(trigger) == AsyncSocketTrigger:
                    await trigger.set(event, data)
                    
                break

    async def start(self):
        await self.connect()

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("*", self.on_event)  # Listen to all events
        
        asyncio.create_task(self.listen())
