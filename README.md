Here's an example of how you can create a class to consume API routes using async programming in Python with the aiohttp library:

import aiohttp
import asyncio

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def get(self, endpoint: str, params: dict = None):
        async with self.session.get(f"{self.base_url}{endpoint}", params=params) as response:
            return await response.json()

    async def post(self, endpoint: str, data: dict):
        async with self.session.post(f"{self.base_url}{endpoint}", json=data) as response:
            return await response.json()

    async def put(self, endpoint: str, data: dict):
        async with self.session.put(f"{self.base_url}{endpoint}", json=data) as response:
            return await response.json()

    async def delete(self, endpoint: str):
        async with self.session.delete(f"{self.base_url}{endpoint}") as response:
            return await response.json()

    async def close(self):
        await self.session.close()

async def main():
    api_client = ApiClient("https://api.example.com/")

    # Get example
    response = await api_client.get("users")
    print(response)

    # Post example
    data = {"name": "John", "age": 30}
    response = await api_client.post("users", data)
    print(response)

    # Put example
    data = {"name": "Jane", "age": 31}
    response = await api_client.put("users/1", data)
    print(response)

    # Delete example
    response = await api_client.delete("users/1")
    print(response)

    await api_client.close()

asyncio.run(main())
In this example, we define an ApiClient class that takes a base_url parameter in its constructor. The class has methods for making GET, POST, PUT, and DELETE requests to the API using the aiohttp library.

Each method uses the async with statement to ensure that the session is properly closed after the request is made. The await keyword is used to wait for the response from the API.

In the main function, we create an instance of the ApiClient class and make some example requests to the API.

Note that you'll need to install aiohttp using pip install aiohttp before running this code.

Also, you can use try-except block to handle errors, and you can add headers, auth, and other parameters to the requests as needed.

You can also use asyncio.gather to make multiple requests concurrently, example:

async def main():
    api_client = ApiClient("https://api.example.com/")

    tasks = [
        api_client.get("users"),
        api_client.post("users", {"name": "John", "age": 30}),
        api_client.put("users/1", {"name": "Jane", "age": 31}),
        api_client.delete("users/1")
    ]

    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)

    await api_client.close()

asyncio.run(main())
This way you can make multiple requests at the same time, and it will improve the performance of your application.

