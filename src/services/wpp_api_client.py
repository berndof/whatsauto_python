import aiohttp
import logging
from typing import Literal, Optional
from config import WPP_API_HOST

class WPPApiClient():    
    
    async def makeRequest(self, method:Literal["POST", "GET"], endpoint:str, headers:Optional[dict]=None, data:Optional[dict]=None):
    
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
    
