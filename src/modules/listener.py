# socket_io_client.py
import asyncio
import socketio

class SocketIOClient:
    def __init__(self, url, manager):
        self.sio = socketio.AsyncClient()
        self.url = url
        self.manager = manager

    async def connect(self):
        await self.sio.connect(self.url)

    async def listen(self):
        try:
            await self.sio.wait()
        except Exception as e:
            print(f"Error listening to events: {e}")

    async def on_connect(self):
        print("Connected to Socket.IO server")

    async def on_disconnect(self):
        print("Disconnected from Socket.IO server")

    async def on_event(self, event, data):
        print(f"Received event: {event} with data: {data}")
        
        if event == "qrCode":
            await self.manager.on_qr_code(event, data)

    async def start(self):
        print("startando")
        await self.connect()
        print("conectado")
        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("*", self.on_event)  # Listen to all events
        asyncio.create_task(self.listen())
