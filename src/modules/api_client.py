import aiohttp
import logging

class ApiClient():
    def __init__(self, host_url):
        self.API_URL = f"{host_url}"
        #self.session = aiohttp.ClientSession()
        
    #async def make_request(self, method, endpoint, headers=None, data=None):
        
    async def make_request(self, method, endpoint, headers=None, data=None):
            async with aiohttp.ClientSession() as session:
                if method == "POST":
                    async with session.post(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                        return await response.json()
                elif method == "GET":
                    async with session.get(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                        return await response.json()
        