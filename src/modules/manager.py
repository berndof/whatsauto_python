from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models
from modules.socket_client import SocketIOClient
import asyncio
import logging
from modules.api_server import FastAPIServer
from typing import Tuple
from modules.bot import Bot
import aiofiles
import os
import json

## manager.py
class Manager(object):
    def __init__(self, api_host:str, secret_key:str, session_name:str) -> None:
        
        self.API_HOST = api_host
        self.SECRET_KEY = secret_key
        self.SESSION_NAME = session_name
        self.SESSION_TOKEN = None
        self.SESSION_STATUS = None
        
        self.api_client = ApiClient(self.API_HOST)
        self.socket_client = SocketIOClient(self.API_HOST, self)
        
        self.api_server = FastAPIServer(self)
        self.qr_code_received = asyncio.Event()
        
        self.session_token_file = "session_token.txt"
    
    async def start(self, environment:str) -> None:
        logging.info(f"starting manager env={environment}")
        
        self.bot = Bot(self, environment)
        
        if environment == "dev" or environment == "prod":
        
            self.db_client = DatabaseClient(environment)
            await self.db_client.create_all()
            
            return 
        else:
            raise ValueError
        
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
        #print(response)
        #check if sucess and etc TODO