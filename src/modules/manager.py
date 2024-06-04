import logging, asyncio, aiofiles, os
from typing import Tuple

from modules.config import TOKEN_FILE_PATH, SESSION_NAME, SECRET_KEY, DEV_PHONE

#rom modules.services.database.test_dal import ChatDAL

#from modules.models import Chat
from modules import services
from modules.bot import Bot



        

class Manager(object):
    
    class WPPSession(object):
        def __load_token(self) -> str | None:
            if os.path.exists(TOKEN_FILE_PATH):
                with open(TOKEN_FILE_PATH, "r") as f:
                    data = f.read()
                    token, name = data.split(":")
                    if name == SESSION_NAME:
                        return token
                    else:
                        return None
                    
        def __load_status(self) -> str:
            if self.token:
                return "CREATED"
            else:
                return "CLOSED"
            
        def __init__(self, name:str) -> None:
                
            self.token = self.__load_token()
            self.status = self.__load_status()
            self.name = name
            
            logging.debug(f"session {self.name} status: {self.status}, token: {self.token} created")
        
        async def store_token(self, token) -> None:
            async with aiofiles.open(TOKEN_FILE_PATH, "w") as f:
                await f.write(f"{token}:{self.name}")
                self.token = token
                return
                

    triggers = []
    is_started = False
    
    def __init__(self) -> None:
        
        self.wpp_api_client = services.WPPApiClient()
        self.wpp_socket_client = services.WPPSocketIOClient(self)
        self.fastapi_server = services.FastAPIServer(self)
        self.db = services.DatabaseClient()
        
        self.bot = Bot(self)
        
        self.session = self.WPPSession(SESSION_NAME)
        
    async def start(self) -> None:        
        
        await self.wpp_socket_client.start()
        #await self.wpp_api_client.start()
        await self.db.start()
        await self.fastapi_server.start()
        
        await self.start_session()
        
        print("sessao pronta")

    async def start_session(self) -> None:
        #TODO change for while
        
        if not self.session.token:
            token = await self.wpp_api_client.get_session_token()
            await self.session.store_token(token)
        
        response = await self.wpp_api_client.start_session(self.session)
        
        if response["status"] == "CONNECTED":
            self.session.status = "CONNECTED"
            return True 
        else:
            self.session.status = "WAITING"
            return await self.wait_qr_scan()
        
    async def wait_qr_scan(self):
        while self.session.status == "WAITING":
            response = await self.wpp_api_client.get_session_status(self.session)
            status = response["status"] 
            if status == "QRCODE":
                qr_data = response["urlcode"] #TODO send qr_data for build qr code
                #scan on wppconnect-server terminal session
                
                logging.debug(f"qr_data: {qr_data}")
                
                self.session.status = "WAITING_SCAN"   
                break
                
            await asyncio.sleep(1) #wait 1 sec to check session status again
            
        #add trigger    
        async def on_session_loged(event, data):
            self.session.status = "CONNECTED"
            return
        
        await self.wpp_socket_client.add_trigger("session-logged", on_catch=on_session_loged)
            
        while self.session.status != "CONNECTED":
            logging.debug("waiting for session loged")
            await asyncio.sleep(1)
        
        return True
        

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