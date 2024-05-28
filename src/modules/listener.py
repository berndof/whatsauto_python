# socket_io_client.py
import asyncio
import socketio

class SocketIOClient:
    def __init__(self, url):
        self.sio = socketio.AsyncClient()
        self.url = url

    async def connect(self):
        await self.sio.connect(self.url)

    async def listen(self):
        await self.sio.wait()

    async def on_connect(self):
        print("Connected to Socket.IO server")

    async def on_disconnect(self):
        print("Disconnected from Socket.IO server")

    async def on_event(self, event, data):
        print(f"Received event: {event} with data: {data}")
        

    async def start(self):
        print("startando")
        await self.connect()
        print("conectado")
        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("*", self.on_event)  # Listen to all events
        await self.listen()
        print("caralho")
