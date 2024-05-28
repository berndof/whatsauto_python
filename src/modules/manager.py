from modules.api_client import ApiClient
from modules.database import DatabaseClient
from modules import models
from modules.listener import SocketIOClient
import asyncio
import qrcode

## manager.py
class Manager():
    def __init__(self):
        
        self.API_URL = "http://localhost:21465/api"
        self.SECRET_KEY = "Sccint002" 
        
        self.session_name = "test_session"
        
        self.api_client = ApiClient(self.API_URL)
        self.socket_io_client = SocketIOClient("http://localhost:21465", self)
        
        self.qr_code_received = asyncio.Event()        
    
    async def _set_database(self, environment):    
        self.db_client = DatabaseClient(environment)
        return await self.db_client.create_all()
        
    def _build_qr(self, qr_data:str): #temporario
        qr = qrcode.QRCode()
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("qrcode.png")
        
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

    async def on_qr_code(self, event, data):
        #print(f"Received qrCode event: {event} with data: {data}")
        self.qr_code_received.set()
        self.data = data 
        
    async def on_received_message(self, event, data):
        response = data["response"]
        try: 
            content = response["content"]
            sender = response["sender"]
            sender_phone = sender["id"].split('@')[0]
            
            if content.lower() == "ping":
                await self.send_message("pong dog", sender_phone)
            
            if content.lower() == "pong":
                await self.send_message("ta pingado, amem", sender_phone)
                
            if "oi" in content.lower():
                message = """
                Você não vai acreditar. Mas você cabia aqui. Eu segurava você e dizia “Esse menino vai ser o melhor menino do mundo. Esse menino vai ser melhor do que qualquer um que conhecemos.”. E você cresceu bom, maravilhoso.

                Aí chegou a hora de você ser adulto e conquistar o mundo. E conquistou. Mas em algum ponto desse percurso, você mudou. Você deixou de ser você.

                Agora deixa as pessoas botarem o dedo na sua cara e dizer que você não é bom. Eu vou te dizer uma coisa que você já sabe: O mundo não é um grande arco-íris. É um lugar sujo, é um lugar cruel. Que não quer saber o quanto você é durão. Vai botar você de joelhos e você vai ficar de joelhos para sempre se você deixar.

                Você, eu, ninguém vai bater tão duro como a vida. Mas não se trata de bater duro. Se trata de quanto você aguenta apanhar e seguir em frente. O quanto você é capaz de aguentar e continuar tentando. É assim que se consegue vencer.

                Agora se você sabe o seu valor, então vá atrás do que você merece. Mas tem que ter disposição para apanhar. E nada de apontar dedos, dizer que você não consegue por causa dele, dela ou de quem seja. Só covardes fazem isso e você não é covarde. Você é melhor do que isso!
                """
                await self.send_message(message, sender_phone)
        except Exception as e:
            print(e)
        
            
    async def send_message(self, message, phone) -> None:
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