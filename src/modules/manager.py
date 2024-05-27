from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models

class Manager():
    def __init__(self):
        self.API_URL = "http://10.4.0.5:21465/api"
        self.SECRET_KEY = "Sccint002" 
        self.api_client = ApiClient(self.API_URL)
        
    async def _set_database(self, environment):    
        self.db_client = DatabaseClient(environment)
        await self.db_client.create_all()
        
    async def create_session(self, session_name):
        #check if session already exists
        #TODO
        exist_session = False
        
        #do api call to create session
        if not exist_session:
            
            ## TODO MAYBE add request body waitQrCode = false
            
            endpoint = f"{session_name}/{self.SECRET_KEY}/generate-token"
            response = await self.api_client.make_request("POST", endpoint)

            if response:
                #TODO implement logging
                print(response)
                token = response["token"]
                status = response["status"]
                #create a whatsappSession Object to store on database
                whatsapp_session = models.WhatsappSession(name=session_name, token=token, status=status)
                
                #call database to store token/session_name and status
                await self.db_client.insert_whatsapp_session(whatsapp_session)        
                
                
                
    async def _test_create_session(self, session_name):
        
        token = "teste"
        status = "testado"
        #create a whatsappSession Object to store on database
        whatsapp_session = models.WhatsappSession(name=session_name, token=token, status=status)
        await self.db_client.insert_whatsapp_session(whatsapp_session)
                