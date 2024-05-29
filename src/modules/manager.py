from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models
from modules.socket_client import SocketIOClient
import asyncio
import logging
from modules.api_server import FastAPIServer
from typing import Tuple
from bot import Bot


## manager.py
class Manager(object):
    def __init__(self, api_host:str, secret_key:str, session_name:str) -> None:
        
        self.API_HOST = api_host
        self.SECRET_KEY = secret_key
        self.SESSION_NAME = session_name
        self.SESSION_TOKEN= "" 
        self.SESSION_STATUS= ""
        
        self.api_client = ApiClient(self.API_HOST)
        self.socket_client = SocketIOClient(self.API_HOST, self)
        
        self.api_server = FastAPIServer(self)
        self.qr_code_received = asyncio.Event()
        
        
    
    async def start(self, environment:str) -> None:
        logging.info(f"starting manager env={environment}")
        if environment == "dev" or environment == "prod":
        
            self.db_client = DatabaseClient(environment)
            await self.db_client.create_all()
            
            return 
        else:
            raise ValueError
        
    async def get_session_token(self) -> Tuple[str, bool, str]:
    
        if self.SESSION_TOKEN != "":
            generated = False
            return self.SESSION_TOKEN, generated, self.SESSION_STATUS
        

        endpoint = f"{self.SESSION_NAME}/{self.SECRET_KEY}/generate-token"
        response = await self.api_client.make_request("POST", endpoint)
        logging.info(response)
        
        if not response: raise NotImplementedError
        if not response["status"] == "success": raise NotImplementedError

        self.SESSION_TOKEN = response["token"]
        self.SESSION_STATUS = "CREATED"
        generated = True
        #deprecated since i will work with 1 session only
        #create a whatsappSession Object 
        #whatsapp_session = models.WhatsappSession(name=session_name, token=token, status=status)
        #await self.db_client.insert_whatsapp_session(whatsapp_session)        

        return self.SESSION_TOKEN, generated, self.SESSION_STATUS

    async def get_session_status(self):
        endpoint = f"{self.SESSION_NAME}/status-session"
        headers = {"Authorization": f"Bearer {self.SESSION_TOKEN}"}
        response = await self.api_client.make_request("GET", endpoint, headers)
        return response
        

    async def start_session(self) -> Tuple[str, str]:
        
        if not self.SESSION_STATUS == "CREATED":
            raise NotImplementedError
        
        endpoint = f"{self.SESSION_NAME}/start-session"
        headers = {"Authorization": f"Bearer {self.SESSION_TOKEN}"}
        response = await self.api_client.make_request("POST", endpoint, headers)
        logging.info(response)
        
        self.SESSION_STATUS = "WAITING"
        is_loged = False
        
        while self.SESSION_STATUS != "QRCODE" and not is_loged:
            response = await self.get_session_status()
            status = response["status"] 
            if status == "QRCODE":
                self.SESSION_STATUS = status
            if status == "CONNECTED":
                is_loged = True
                self.SESSION_STATUS = status 
            await asyncio.sleep(5)

        qr_data = None
        if not is_loged:
            qr_data = response["urlcode"]
            
            # set a trigger to listen for event of session logged in
            self.wait_scan_confirm_event = True
            
        return self.SESSION_STATUS, qr_data

    
    async def on_session_loged(self, event, data):

        if self.wait_scan_confirm_event:
            # se o trigger for acionado
            logging.info("")
            self.SESSION_STATUS = "CONNECTED"
            pass
        
        
    async def on_received_message(self, event, data):
        
        response = data["response"]
        message = response["content"]
        
        if message.lower() == "ping":
            await self.send_message("pong", response["sender"]["id"].split('@')[0])
        
        #send message to automations
        else:
            start_chat_triage
        
            
    async def send_message(self, message:str, phone:str) -> None:
        exists_session = await self.db_client.get_whatsapp_session_by_name(self.session_name)
        
        endpoint = f"{self.session_name}/send-message"
        body = {
            "phone": f"{phone}",
            "isGroup": False,
            "isNewsletter": False,
            "message": f"{message}"
        }
        headers = {
            'accept': '*/*',
            'Authorization': 'Bearer $2b$10$wuy4_YHe38Wi9Y6H8BNtLOXt6Fj29QOrg_PtkV6L3rVUwr2ohADly',
            'Content-Type': 'application/json'
        }
        response = await self.api_client.make_request("POST", endpoint, headers, body)
        print(response)
        #check if sucess and etc TODO