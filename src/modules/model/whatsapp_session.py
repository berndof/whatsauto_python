from modules.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class WhatsappSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    token = Column(String)
    #Created_at
    #Updated_at
    #Created_by
    #...

    def __repr__(self):
        return f"<Session(id={self.id}, name={self.name}, token={self.token})>"