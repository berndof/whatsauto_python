
import logging

ENV = "dev"
DEV_PHONE = 554999564665

TOKEN_FILE_PATH="./src/data/sessions.txt"

SESSION_NAME = "dev"
SECRET_KEY = "Sccdev76"

FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = 8000

WPP_API_HOST = "http://localhost:21465"

DATABASE_URL = "sqlite://db.sqlite3"

logging.basicConfig(level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S")
logging.info("log level set to debug")