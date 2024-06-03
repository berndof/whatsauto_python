import asyncio
import logging
from typing import Tuple
import aiofiles
import os
from automations.bot import Bot
from automations.triggers.socket_trigger import SocketTrigger

class WPPSession(object):
    def __init__(self, name:str, token:str|None, status:str="CLOSED") -> None:
        logging.info(f"init session: name={name}, token={token}")
        
        self.name = name
        #TODO checar se a sessão não esta salva no arquivo para buscar o token
        self.token = token
        
        self.status = status

class Manager(object):
    def __init__(self, config:dict) -> None:
        
        self.__setup_services(config)
        
        self.__create_session(config)
        self.token_file_path = config["token_file_path"]
        
        #*temporary
        self.dev_phone = config["dev_phone"]
        
        self.__get_secret_key(config)
        
        self.triggers = []
        
        self.is_started = False
        
    def __setup_services(self, config:dict):
        # wpp api client
        from modules.services.wpp_api_client import WPPApiClient
        self.wpp_api_client = WPPApiClient(config["api_host"])
        
        #wpp socket client
        from modules.services.wpp_socket_client import WPPSocketIOClient
        self.wpp_socket_client = WPPSocketIOClient(config["api_host"], self)
        
        #fastapi server
        from modules.services.fastapi_server import FastAPIServer
        self.fastapi_server = FastAPIServer(self, config["fastapi_host"], config["fastapi_port"])
        
        #database client
        database_config = config["database"]
        from modules.services.database_client import DatabaseClient
        self.db_client = DatabaseClient(environment=config["environment"], config=database_config)
        
        from automations.bot import Bot
        self.bot = Bot(self)
        
    def __create_session(self, config:dict):
        #check if session and token already saved on file and get token from file
        token_file_path = config["token_file_path"]
        logging.debug(f"token_file_path={token_file_path}")
        if os.path.exists(token_file_path):
            with open(token_file_path, "r") as f:
                data = f.read()
                token, name = data.split(":")
                if name == config["session_name"]:
                    self.session = WPPSession(name=config["session_name"], token=token, status="CREATED")
                else:
                    # TODO delete token file
                    pass       
        else:
            self.session = WPPSession(name=config["session_name"], token=None)
        
    def __get_secret_key(self, config:dict):
        self.SECRET_KEY = config["secret_key"]
        
    async def start(self) -> None:        

            await self.db_client.start()
            await self.fastapi_server.start()
            await self.wpp_socket_client.start()
            await self.wpp_api_client.start()

            if self.session.status == "CLOSED":
                self.session.token = await self.__get_session_token()
            
            #here self.session.status must have to be "CREATED" and a token must be created and stored
            #then
            await self.start_session()
            #here self.session.status must have to be "CONNECTED" if not i dont now what to do (for now)
            await self.send_message("Hello World!")
            #TODO check if message was recieved | implement tests 
            
            self.is_started = True
            
            #now that all the services are started i can start bot (what does this means?)
            await self.bot.start()

    #TODO this method on WhatsappSession class
    async def __get_session_token(self) -> Tuple[str, bool, str]:
            
        endpoint = f"{self.session.name}/{self.SECRET_KEY}/generate-token"
        response = await self.wpp_api_client.make_request("POST", endpoint)
        logging.debug(response)
        
        if not response: raise NotImplementedError("response not received")
        if not response["status"] == "success": raise NotImplementedError("response recived was not success check wpp-server logs")
        
        token = response["token"]
        
        self.session.status = "CREATED"
        self.session.token = token

        #store token in a file
        data_to_store=f"{token}:{self.session.name}"
        
        async with aiofiles.open(self.token_file_path, "w") as f:
            await f.write(data_to_store)
        return token 

    async def __get_session_status(self):
        endpoint = f"{self.session.name}/status-session"
        headers = {"Authorization": f"Bearer {self.session.token}"}
        response = await self.wpp_api_client.make_request("GET", endpoint, headers)
        return response
        
    async def add_trigger(self, trigger) -> SocketTrigger:
        logging.debug(f"adding trigger {trigger.name}")
        self.triggers.append(trigger)
        return trigger   

        
    async def start_session(self) -> Tuple[str, str]:
        
        endpoint = f"{self.session.name}/start-session"
        headers = {"Authorization": f"Bearer {self.session.token}"}
        response = await self.wpp_api_client.make_request("POST", endpoint, headers)
        
        if response["status"] == "CONNECTED":
            self.session.status = "CONNECTED"
        else: self.session.status = "WAITING"
        
        while self.session.status == "WAITING":
            response = await self.__get_session_status()
            status = response["status"] 
            
            if status == "QRCODE":

                qr_data = response["urlcode"]
                #TODO send qr_data to frontend for build qr then wait for qr_scan 
                #by now scan qr from wpp-server console
                
                # set a trigger to listen for event of session logged in

                def on_catch(self, event, data):
                    self.session.status = "CONNECTED"
                    return
                
                trigger = SocketTrigger("wait_for_qr_scan", "session_logged", on_catch)
                await self.add_trigger(trigger)
                
            #satys on loop until status is "CONNECTED"
            if status == "CONNECTED":
                break
                
            await asyncio.sleep(1) #wait 1 sec to check session status again
            
        return 
    
    #*test method
    async def send_message(self, message:str) -> None:
        
        endpoint = f"{self.session.name}/send-message"
        body = {
            "phone": f"{self.dev_phone}",
            "isGroup": False,
            "isNewsletter": False,
            "message": f"{message}"
        }
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {self.session.token}',
            'Content-Type': 'application/json'
        }
        response = await self.wpp_api_client.make_request("POST", endpoint, headers, body)
        print(response)
        #check if sucess and etc TODO
        
    async def close(self) -> None:
        await self.db_client.close()
        await self.fastapi_server.close()
        await self.wpp_socket_client.close()
        await self.wpp_api_client.close()#
        
        loop = asyncio.get_event_loop()
        loop.stop()