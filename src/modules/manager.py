from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models
from modules.socket_client import SocketIOClient
import asyncio
import qrcode
import logging

## manager.py
class Manager():
    def __init__(self, api_host:str, secret_key:str, session_name:str) -> None:
        
        self.API_HOST = api_host
        self.SECRET_KEY = secret_key
        self.SESSION_NAME = session_name
        self.TOKEN:str 
        self.STATUS:str
        
        self.api_client = ApiClient(self.API_HOST)
        self.socket_client = SocketIOClient(self.API_HOST, self)
        
        self.qr_code_received = asyncio.Event()        
    
    async def start(self, environment:str) -> None:
        logging.info(f"starting manager env={environment}")
        if environment == "dev" or environment == "prod":
            self.db_client = DatabaseClient(environment)
            await self.db_client.create_all()
            return 
        else:
            raise ValueError
        
    async def generate_token(self):
    
        endpoint = f"/{self.SESSION_NAME}/{self.SECRET_KEY}/generate-token"
        response = await self.api_client.make_request("POST", endpoint)
        logging.info(response)
        if not response: raise NotImplementedError
                
        if not response["status"] == "success": raise NotImplementedError

        self.TOKEN = response["token"]
        self.STATUS = "CREATED"
        
        #deprecated since i will work with 1 session only
        #create a whatsappSession Object 
        #whatsapp_session = models.WhatsappSession(name=session_name, token=token, status=status)
        #await self.db_client.insert_whatsapp_session(whatsapp_session)        

        return self.TOKEN

    async def start_session(self, session_name:str):
        #check if session already exists
        #in database or in api?
        
        #checkin in database
        exists_session = await self.db_client.get_whatsapp_session_by_name(session_name)

        if not exists_session: return None #raise exception?
        
        endpoint = f"{session_name}/start-session"
        headers = {"Authorization": f"Bearer {exists_session.token}"}
        response = await self.api_client.make_request("POST", endpoint, headers)
        print(response)
        
        #DONT NEED MORE BUT ITS WORKING
        #here i need to wait for a qrCode event of listener.py
        """ print("wait for event qrCode")
        await self.qr_code_received.wait()
        
        if self.data["session"] == session_name:
            print("make request to get qr_data") """
        
        status = "CLOSED"
        endpoint = f"{session_name}/status-session"
        
        while status != "QRCODE":
            response = await self.api_client.make_request("GET", endpoint, headers)
            if not response:
                continue
            status = response["status"]
            await asyncio.sleep(1)

        qr_data = response["urlcode"]
        
        self._build_qr(qr_data)

        #await confirmation of login 
        #Received event: session-logged with data: {'status': True, 'session': 'test_session'}

        return

    async def temp_test(self):
        print("alo")
        await asyncio.sleep(1)

    async def on_received_message(self, event, data):
        #check if event is the right one
        response = data["response"]
        try: 
            content = response["content"]
            sender = response["sender"]
            sender_phone = sender["id"].split('@')[0]
            
            if content.lower() == "ping":
                await self.send_message("pong", sender_phone)
            
        except Exception as e:
            print(e)
        
            
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