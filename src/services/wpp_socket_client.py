# wpp_socket_client.py
import asyncio, socketio, logging
from config import WPP_API_HOST
from typing import List

class WPPSocketIOClient(object):

    class SocketTrigger(object):
        def __init__(self, event_to_catch:str, on_catch:callable) -> None:
            self.event_to_catch = event_to_catch
            self.on_catch = on_catch
            logging.debug(f"creating a trigger for event {self.event_to_catch}")

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __repr__(self) -> str:
            return f"waiting for {self.event_to_catch} event"

        async def set(self, event, data):
            logging.info(f"trigger set | {self.event_to_catch}")

            await self.on_catch(event, data)
            return

    def __init__(self, manager) -> None:
        self.sio = socketio.AsyncClient()
        self.manager = manager
        self.triggers:List[self.SocketTrigger] = []

    async def connect(self) -> None:
        try:
            await self.sio.connect(WPP_API_HOST)
            logging.info("connecting to socket")
        except Exception as e:
            logging.error(f"failed to connect to socket: {e}")

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
        logging.debug(f"event recieved: {event}") #HERE

        for trigger in self.triggers:
            logging.debug(f"checking: {trigger}")

            if trigger.event_to_catch == str(event):
                await trigger.set(event, data)
            else:
                logging.debug(f"trigger not matching: {trigger.event_to_catch} != {event}")
                continue

    async def start(self):
        await self.connect()

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("*", self.on_event)  # Listen to all events

    async def add_trigger(self, event_to_catch:str, on_catch:callable) -> None:
        trigger = self.SocketTrigger(event_to_catch, on_catch)

        if trigger not in self.triggers:
            self.triggers.append(trigger)
            logging.debug(f"trigger added: {trigger}")
        else:
            logging.debug(f"trigger already exists: {trigger}")

        return
