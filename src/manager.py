import logging, asyncio, aiofiles, os
from config import TOKEN_FILE_PATH, SESSION_NAME, ENV, DEV_PHONE
import services
import bot



        

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
    
    def __init__(self) -> None:
        
        self.wpp_api_client = services.WPPApiClient()
        self.wpp_socket_client = services.WPPSocketIOClient(self)
        self.fastapi_server = services.FastAPIServer(self)
        self.db = services.DatabaseClient()
        self.session = self.WPPSession(SESSION_NAME)
        self.bot = bot.Bot(self)
        
    async def start(self) -> None:        
        
        await self.db.start()
        await self.wpp_socket_client.start()
        await self.fastapi_server.start()
        
        await self.__start_session()

        await self.bot.startListenMessages()

    async def __start_session(self) -> None:
        #TODO change for while
        
        if not self.session.token:
            token = await self.__get_session_token()
            await self.session.store_token(token)
        
        #response = await self.wpp_api_client.start_session(self.session)
        
        endpoint = f"{self.session.name}/start-session"
        headers = {"Authorization": f"Bearer {self.session.token}"}
        response =  await self.wpp_api_client.makeRequest("POST", endpoint, headers) 
        logging.debug(f"session {self.session.name} status: {response['status']}")
        
        if response["status"] == "CONNECTED":
            self.session.status = "CONNECTED"
            return True 
        else:
            self.session.status = "WAITING"
            return await self.__wait_qr_scan()
        
    async def __get_session_token(self):
        endpoint = f"{self.session.name}/status-session"
        headers = {"Authorization": f"Bearer {self.session.token}"}
        return await self.wpp_api_client.makeRequest("GET", endpoint, headers)

    async def __wait_qr_scan(self):
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

    async def sendMessage(self, chat, message):
        endpoint = f"{self.session.name}/send-message"
        
        if ENV == "dev" and chat.phone != DEV_PHONE:
            logging.debug(f"ignoring message from {chat.phone} because it is not dev phone")
            return
        
        body = {
            "phone": f"{chat.phone}",
            "message": f"{message}"
        }
        
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {self.session.token}',
            'Content-Type': 'application/json'
        }
        return await self.wpp_api_client.makeRequest("POST", endpoint, headers, body)
        
    async def close(self) -> None:
        await self.db_client.close()
        await self.fastapi_server.close()
        await self.wpp_socket_client.close()
        await self.wpp_api_client.close()#
        
        loop = asyncio.get_event_loop()
        loop.stop()