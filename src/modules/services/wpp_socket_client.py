# wpp_socket_client.py
import asyncio
import socketio
import logging

class WPPSocketIOClient:
    event_mapper = {
        #event:method on manager
        "received-message": "on_received_message",
        "session-logged": "on_session_loged"
    }
    
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
        logging.info(f"event recieved: {event}")
        try:
            #busca no event mapper o nome da função para chamar no manager 
            method_name = self.event_mapper.get(event)
            method = getattr(self.manager, method_name)
            logging.debug(f"calling method {method_name} on manager")
            await method(event, data)
        except:
            pass

    async def start(self):
        await self.connect()

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("*", self.on_event)  # Listen to all events
        
        asyncio.create_task(self.listen())
