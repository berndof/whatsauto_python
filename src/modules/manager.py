import asyncio
import logging
from typing import Tuple
import aiofiles
import os

class Session(object):
    def __init__(self, name:str, token:str|None) -> None:
        logging.info(f"init session: name={name}, token={token}")
        
        self.name = name
        #TODO checar se a sessão não esta salva no arquivo para buscar o token
        self.token = token
        
        self.status = "CLOSED"

class Manager(object):
    def __init__(self, config:dict) -> None:
        
        self.__setup_services(config)
        
        # GENERAL ATTRIBUTES
        self.SECRET_KEY = config["secret_key"]
        
        #create session without token
        self.session = Session(config["session_name"], None)    
        
        #Trigger events   TODO tirar daqui
        self.qr_code_received = asyncio.Event()
        
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
        
    async def start(self) -> None:        

            await self.db_client.start()
            await self.fastapi_server.start()
            await self.wpp_socket_client.start()
            await self.db_client.start()
            
            #self.session.token = await self.wpp_api_client.get_session_token()
            

        
    async def get_session_token(self) -> Tuple[str, bool, str]:
        if os.path.exists(self.session_token_file):
            async with aiofiles.open(self.session_token_file, "r") as f:
                data = await f.read()
                token, name = data.split(":")
                if name == self.SESSION_NAME:
                    self.SESSION_STATUS = "CREATED"
                    return token
                else:raise NotImplementedError
            
        endpoint = f"{self.SESSION_NAME}/{self.SECRET_KEY}/generate-token"
        response = await self.api_client.make_request("POST", endpoint)
        
        if not response: raise NotImplementedError
        if not response["status"] == "success": raise NotImplementedError
        token = response["token"]
        
        self.SESSION_STATUS = "CREATED"
        self.SESSION_TOKEN = token

        #store token in a file
        data_to_store=f"{token}:{self.SESSION_NAME}"
        async with aiofiles.open(self.session_token_file, "w") as f:
            await f.write(data_to_store)
        return token 

    async def get_session_status(self):
        endpoint = f"{self.SESSION_NAME}/status-session"
        headers = {"Authorization": f"Bearer {self.SESSION_TOKEN}"}
        response = await self.api_client.make_request("GET", endpoint, headers)
        return response
        
    async def start_session(self) -> Tuple[str, str]:
        
        if not self.SESSION_TOKEN:
            self.SESSION_TOKEN = await self.get_session_token()
        
        if self.SESSION_STATUS != "CREATED":
            return self.SESSION_STATUS, None
        
        endpoint = f"{self.SESSION_NAME}/start-session"
        headers = {"Authorization": f"Bearer {self.SESSION_TOKEN}"}
        response = await self.api_client.make_request("POST", endpoint, headers)
        
        self.SESSION_STATUS = "WAITING"
        
        while self.SESSION_STATUS == "WAITING":
            response = await self.get_session_status()
            status = response["status"] 
            if status == "QRCODE":
                self.SESSION_STATUS = status
                qr_data = response["urlcode"]
                # set a trigger to listen for event of session logged in
                self.wait_scan_confirm_event = True
            if status == "CONNECTED":
                qr_data = None
                self.SESSION_STATUS = status 
            await asyncio.sleep(1)
                        
        return self.SESSION_STATUS, qr_data

    async def on_session_loged(self, event, data):

        if self.wait_scan_confirm_event:
            # se o trigger for acionado
            logging.info("wait_scan event triggered")
            self.SESSION_STATUS = "CONNECTED"
            pass
        
    async def on_received_message(self, event, data):
        
        response = data["response"]
        logging.info (f"message received: {response}")
        
        message = response["content"]

        #send message to automations
        #else:
        if message != "":
            await self.bot.on_message(response)
        
    async def send_message(self, message:str, phone:str) -> None:
        
        endpoint = f"{self.SESSION_NAME}/send-message"
        body = {
            "phone": f"{phone}",
            "isGroup": False,
            "isNewsletter": False,
            "message": f"{message}"
        }
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {self.SESSION_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = await self.api_client.make_request("POST", endpoint, headers, body)
        print(response)
        #check if sucess and etc TODO