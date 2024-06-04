import aiohttp
import logging
from typing import Literal, Optional
from modules.config import WPP_API_HOST, SECRET_KEY, SESSION_NAME

class WPPApiClient():    
    
    async def __make_request(self, method:Literal["POST", "GET"], endpoint:str, headers:Optional[dict]=None, data:Optional[dict]=None):
    
        async with aiohttp.ClientSession() as session:
            if method == "POST":
                
                url = f"{WPP_API_HOST}/api/{endpoint}"
                logging.debug(f"making a POST request to {url}, headers: {headers}, data: {data}")
                try:
                    async with session.post(url, headers=headers, json=data) as response:
                        return await response.json()
                except Exception as e:
                    logging.error(f"failed to make a POST request: {e}")
                    return None
                
            elif method == "GET":
                url = f"{WPP_API_HOST}/api/{endpoint}"
                logging.debug(f"making a GET request to {url}, headers: {headers}, data: {data}")
                try:
                    async with session.get(url, headers=headers, json=data) as response:
                        return await response.json()
                except Exception as e:
                    logging.error(f"failed to make a GET request: {e}")
                    return None
    
    async def get_session_token(self):
        endpoint = f"{SESSION_NAME}/{SECRET_KEY}/generate-token"
        return await self.__make_request("POST", endpoint)
        
    async def start_session(self, session):
        endpoint = f"{session.name}/start-session"
        
        headers = {"Authorization": f"Bearer {session.token}"}
        
        response =  await self.__make_request("POST", endpoint, headers) 
        
        logging.debug(f"session {session.name} status: {response['status']}")
        print(response)
        return response

    async def get_session_status(self, session):
        endpoint = f"{session.name}/status-session"
        headers = {"Authorization": f"Bearer {session.token}"}
        return await self.__make_request("GET", endpoint, headers)