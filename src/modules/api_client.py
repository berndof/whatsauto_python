import aiohttp

class ApiClient():
    def __init__(self, api_url):
        self.API_URL = api_url
        self.session = aiohttp.ClientSession()
        
    async def make_request(self, method, endpoint, headers=None, data=None):
        
        if not endpoint:
            return None
            #raise a exception TODO
            #aiohttp.client_exeptions.ClientConnectorError
            
        if method == "POST":
            async with self.session.post(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                return await response.json()
        
        if method == "GET":
            async with self.session.get(f"{self.API_URL}{endpoint}", headers=headers, json=data) as response:
                return await response.json()
    
    async def close(self):
        await self.session.close()