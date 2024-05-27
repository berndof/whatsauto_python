from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models
import asyncio


class Manager():
    def __init__(self):
        self.API_URL = "http://10.4.0.5:21465/api"
        self.SECRET_KEY = "Sccint002" 
        self.api_client = ApiClient(self.API_URL)
    
    async def _set_database(self, environment):    
        self.db_client = DatabaseClient(environment)
        await self.db_client.create_all()
    
    async def _close_database_connector(self):
        await self.db_client.close()
    
    async def create_session(self, session_name):
        #check if session already exists
        #TODO
        exist_session = False
        
        #do api call to create session
        if exist_session:
            return False
            #TODO raise exception ?
            
        ## TODO MAYBE add request body waitQrCode = false
        endpoint = f"{session_name}/{self.SECRET_KEY}/generate-token"
        response = await self.api_client.make_request("POST", endpoint)

        if not response:
            return False
            #TODO raise exception?
                
        #TODO implement logging
        print(response)
        
        if not response["status"] == "success":
            return False

        token = response["token"]
        status = "TOKEN_GENERATED"
        
        #create a whatsappSession Object to store on database
        whatsapp_session = models.WhatsappSession(name=session_name, token=token, status=status)
        
        #call database to store token/session_name and status
        await self.db_client.insert_whatsapp_session(whatsapp_session)        

        return

    async def start_session(self, session_name):
        #check if session already exists
        #in database or in api?
        
        #checkin in database
        exists_session = await self.db_client.get_whatsapp_session_by_name(session_name)

        if not exists_session:
            return None
            #TODO raise error
            
        if not exists_session.status == "TOKEN_GENERATED":
            return None
            #TODO raise error
        
        print(exists_session)
        #<Session(id=2, name=test_sesssion, token=$2b$10$v1G.A9z27odQFGe2RQezW.t_kOwbNnQaRGxBDaq2mAj8Pn6aIoXsO)>
        
        #if exists, check on api to confirm status is disconnected
        #TODO
        
        endpoint = f"{session_name}/status-session"
        headers = {"Authorization": f"Bearer {exists_session.token}"}    

        status = None
        
        max_retries = 10
        attempt = 0
        status = None

        # CLOSED -> INITIALIZING -> CLOSED -> QRCODE


        while status != "QRCODE" and attempt < max_retries:
            try:
                response = await self.api_client.make_request("GET", endpoint, headers=headers)
                if not response:
                    attempt += 1
                    continue
                status = response["status"]
                print(response)
            except Exception as e:
                print(f"Encountered an error: {e}")
                attempt += 1
            await asyncio.sleep(1)

        if attempt >= max_retries:
            raise Exception("Max retries reached. QR Code not received.")

        if status == "QRCODE":
            qr_data = response["urlcode"]
            print(qr_data)
            input("Press Enter to stop...")
                
        
        