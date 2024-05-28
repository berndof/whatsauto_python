import asyncio
from modules.manager import Manager

async def main():
    manager = Manager() 
    #
    await manager._set_database("dev")
    #print("passei daqui ")
    #await manager.socket_io_client.start()
    #print("Started listener")

    await manager.test_send_message()

    # Test generate_token and start_session
    #await manager.generate_token("test_session")
    #await manager.start_session("test_session")

    # Keep the event loop running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())