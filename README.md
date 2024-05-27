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

___

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatabaseClient:
    def __init__(self, environment, DB_HOST=None, DB_PORT=None, DB_USER=None, DB_PASSWORD=None, DB_NAME=None):
        self.engine = create_async_engine(
            self._construct_db_url(environment, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME),
            echo=True,  # You can set this to False to reduce logging
        )
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def _construct_db_url(self, environment, DB_HOST, DB_PORT, DB_user, DB_PASSWORD, DB_NAME):
        if environment == "dev" or not environment:
            return "sqlite+aiosqlite:///db.sqlite"
        elif environment == "prod":
            return f"postgresql+asyncpg://{DB_user}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:
            raise ValueError("Invalid environment")

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self):
        # Each call to get_session will provide a new session
        return self.Session()

    # Placeholder methods for CRUD operations
    async def add_record(self, record):
        pass

    async def get_records(self):
        pass

    async def update_record(self, record):
        pass

    async def delete_record(self, record):
        pass

    # Placeholder for migration handling
    async def run_migrations(self):
        pass

    # Placeholder for error handling
    async def handle_errors(self):
        pass
This updated class provides a structure that you can further develop as you build out your application. It includes placeholders for CRUD operations, migration handling, and error handling. You can implement the logic for these methods as needed when you define your models in models.py.

The create_all method is already set up to create your tables asynchronously based on the Base.metadata definitions in your models. The get_session method will provide a new session for each database operation, which can be used in manager.py for database interactions.

As you mentioned you're not very familiar with async programming, remember that when you call any of the async methods in DatabaseClient, you'll need to await them to ensure they run as part of the event loop. This is crucial to maintain the non-blocking behavior of your application.

# manage.py
import asyncio
from database import DatabaseClient
from models import User, Base

async def main():
    # Initialize the DatabaseClient
    db_client = DatabaseClient(environment="dev")
    
    # Create the database tables
    await db_client.create_all()

    # Create a new user instance
    new_user = User(name="Alice", age=25)
    
    # Add the new user record to the database
    async with db_client.get_session() as session:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        print(f"Added new user: {new_user}")

    # Retrieve a user record from the database
    async with db_client.get_session() as session:
        user = await session.get(User, new_user.id)
        print(f"Retrieved user: {user}")

    # Update a user record in the database
    async with db_client.get_session() as session:
        user_to_update = await session.get(User, new_user.id)
        user_to_update.age = 26  # Update the age
        await session.commit()
        print(f"Updated user: {user_to_update}")

    # Delete a user record from the database
    async with db_client.get_session() as session:
        user_to_delete = await session.get(User, new_user.id)
        await session.delete(user_to_delete)
        await session.commit()
        print(f"Deleted user: {user_to_delete}")

# Run the main coroutine
asyncio.run(main())

___