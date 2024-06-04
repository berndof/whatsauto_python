from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

ENVIRONMENT_CONFIG = {
    "environment": "dev",
    "debug": True,
    "secret_key": "Sccdev76",
    "session_name": "dev",
    "wpp_api_host": "http://localhost:21465",
    "fastapi_port": 8000,
    "fastapi_host": "0.0.0.0",
    "dev_phone": "554999564665" #as string
}
DEV_PHONE = "554999564665"

TOKEN_FILE_PATH="./src/data/sessions.txt"

SESSION_NAME = "dev"
SECRET_KEY = "Sccdev76"

FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = 8000

WPP_API_HOST = "http://localhost:21465"

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

