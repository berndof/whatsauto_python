import asyncio
import logging
import yaml
import os

def load_config(config_file_path:str) -> dict:
    """Loads configuration from config.yaml and set log level

    Raises:
        FileNotFoundError: if config file not found

    """

    if not os.path.exists(config_file_path):
        logging.info("config file not found")
        raise FileNotFoundError

    with open(config_file_path, "r") as f:
        config = yaml.safe_load(f)
        
    if config["debug"]:
        logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")
        logging.info("log level set to debug")
        
    else:
        logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")
        logging.info("log level set to info")
    
    logging.info("config loaded")
        
    return config

async def main():
    
    # * WORKING HERE
    await manager.start() #set db, start the consumer ..
    
    # Keep the event loop running 
    # TODO i think this loop can be replaced for some async loop function like run forever
    
    """while True:
        await asyncio.sleep(1)"""
        
if __name__ == "__main__":
    
    config_file_path = "src/config.yaml"
    config = load_config(config_file_path)

    from modules.manager import Manager
    manager = Manager(config) 

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_forever()

    asyncio.run