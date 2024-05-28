import logging
import asyncio
from modules.manager import Manager
from modules.listener import SocketIOClient

logging.basicConfig(level=logging.INFO)

async def main():
    manager = Manager()
    asyncio.get_event_loop().set_debug(True)
    socket_io_client = SocketIOClient("http://localhost:21465")

    async def callback(event, data):
        # Call the corresponding method in the Manager class
        """ if event == "session_status":
            await manager.on_session_status(data)
        elif event == "message_received":
            await manager.on_message_received(data) """
        # Add more event handlers as needed
        print(f"event: {event}\n data: {data}")

    #await manager._set_database("dev")

    # Start the Socket.IO client with the callback function
    await socket_io_client.start(callback)
    # logging.info(f"Creating session: {session_name}")

    # Start the session
    #await manager.start_session("test_session")

    # Keep the event loop running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())