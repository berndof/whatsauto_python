

from typing import List, Optional
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from modules import models

class ChatDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_chat(self, name: str):
        new_chat = models.Chat(name=name)
        self.db_session.add(new_chat)
        await self.db_session.flush()