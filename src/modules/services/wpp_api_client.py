import aiohttp
import logging
from typing import Literal, Optional

class WPPApiClient():
    def __init__(self, host_url):
        self.host_url = f"{host_url}"
        self.is_started = False
        
    async def start(self):
        self.is_started = True
        return self.is_started
        
    async def make_request(self, method:Literal["POST", "GET"], endpoint:str, headers:Optional[dict]=None, data:Optional[dict]=None):
        if not self.is_started:
            raise NotImplementedError("WPPApiClient is not started")
        
        else:
            async with aiohttp.ClientSession() as session:
                if method == "POST":
                    url = f"{self.host_url}/api/{endpoint}"
                    logging.debug(f"making a POST request to {url}, headers: {headers}, data: {data}")
                    async with session.post(url, headers=headers, json=data) as response:
                        return await response.json()
                elif method == "GET":
                    url = f"{self.host_url}/api/{endpoint}"
                    logging.debug(f"making a GET request to {url}, headers: {headers}, data: {data}")
                    async with session.get(url, headers=headers, json=data) as response:
                        return await response.json()
        