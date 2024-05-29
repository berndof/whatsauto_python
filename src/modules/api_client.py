import aiohttp
import logging

class ApiClient():
    def __init__(self, host_url):
        self.API_URL = f"{host_url}/api"
        self.session = aiohttp.ClientSession()
        
    async def make_request(self, method, endpoint, headers=None, data=None):
        
        if not endpoint:
            logging.error("Cant make a request without a endpoint")
            raise ValueError
        
        if method == "POST":
            logging.info(f"sending POST request \n endpoint: {endpoint} \n headers: {headers} \n body: {data} ")
            async with self.session.post(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                return await response.json()
        
        if method == "GET":
            logging.info(f"sending GET request \n endpoint: {endpoint} \n headers: {headers} \n body: {data} ")
            async with self.session.get(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                return await response.json()
    