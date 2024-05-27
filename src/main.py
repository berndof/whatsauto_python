from modules.manager import Manager
import asyncio

async def main():
    manager = Manager()
    
    session_name = "test_sesssion"
    
    await manager._set_database("dev")
    #await asyncio.sleep(1)
    
    #rotina para consumir o manager
    #await manager.create_session(session_name)
    #await manager._test_create_session("test_session")
    #await asyncio.sleep(2)
    
    await manager.start_session(session_name)
    await asyncio.sleep(1)
    
    await manager._close_database_connector()

if __name__ == "__main__":
    asyncio.run(main())