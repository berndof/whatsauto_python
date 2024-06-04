import asyncio
import logging
import yaml
import os



async def main():
    
    # * WORKING HERE
    await manager.start() #set db, start the consumer ..
    
    # Keep the event loop running 
    # TODO i think this loop can be replaced for some async loop function like run forever
    
    while True:
        await asyncio.sleep(1)
        
if __name__ == "__main__":
    from modules.manager import Manager
    manager = Manager() 

    #loop = asyncio.new_event_loop()
    #task = asyncio.create_task(main())
    #task.run_forever()
    asyncio.run(main())

