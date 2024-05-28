from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models
from modules.listener import SocketIOClient
import asyncio

class Manager():
    def __init__(self):
        
        self.API_URL = "http://localhost:21465/api"
        self.SECRET_KEY = "Sccint002" 
        
        self.api_client = ApiClient(self.API_URL)
        self.socket_io_client = SocketIOClient("http://localhost:21465")
        
    
    async def _set_database(self, environment):    
        self.db_client = DatabaseClient(environment)
        return await self.db_client.create_all()
        
    async def generate_token(self, session_name):
        print("gerando token")
        #TODO check if session already exists
        exist_session = False
        if exist_session: return False #raise exception ?
        
        #generate token
        endpoint = f"{session_name}/{self.SECRET_KEY}/generate-token"
        response = await self.api_client.make_request("POST", endpoint)
        print(response)
        if not response: return False #raise exception?
                
        print(f"response: {response}")
        
        if not response["status"] == "success": return False #raise exception?

        token = response["token"]
        status = "TOKEN_GENERATED"
        
        #create a whatsappSession Object
        whatsapp_session = models.WhatsappSession(name=session_name, token=token, status=status)
        await self.db_client.insert_whatsapp_session(whatsapp_session)        

        return True

    async def start_session(self, session_name):
        #check if session already exists
        #in database or in api?
        
        #checkin in database
        exists_session = await self.db_client.get_whatsapp_session_by_name(session_name)

        if not exists_session: return None #raise exception?
        
        endpoint = f"{session_name}/start-session"
        headers = {"Authorization": f"Bearer {exists_session.token}"}
        response = await self.api_client.make_request("POST", endpoint, headers)
        
        #here i need to wait for a qrCode event of listener.py
        print("wait for event qrCode")

        
        return

    async def on_qr_code_event(self, data):
        # Handle QR code event from listener
        print("Received QR code event")
        # Set event flag
        self.socket_io_client.qr_code_event.set()
        
        