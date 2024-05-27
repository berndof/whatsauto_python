from modules.manager import Manager
import asyncio

async def main():
    manager = Manager()


    await manager._set_database("dev")
    #rotina para consumir o manager
    #await manager.create_session("test_session")
    await manager._test_create_session("test_session")

if __name__ == "__main__":
    asyncio.run(main())