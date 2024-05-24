from modules.manager import Manager
import asyncio

async def main():
    manager = Manager()

    #rotina para consumir o manager
    await manager.create_session("test_session")


if __name__ == "__main__":
    asyncio.run(main())