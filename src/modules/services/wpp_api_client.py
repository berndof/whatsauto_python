import aiohttp
import logging

class WPPApiClient():
    def __init__(self, host_url):
        self.API_URL = f"{host_url}"
        
    async def make_request(self, method, endpoint, headers=None, data=None):
            async with aiohttp.ClientSession() as session:
                if method == "POST":
                    logging.debug(f"making a POST request to {self.API_URL}/{endpoint}")
                    async with session.post(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                        return await response.json()
                elif method == "GET":
                    logging.debug(f"making a GET request to {self.API_URL}/{endpoint}")
                    async with session.get(f"{self.API_URL}/{endpoint}", headers=headers, json=data) as response:
                        return await response.json()
        