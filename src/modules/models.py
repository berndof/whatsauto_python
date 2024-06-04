from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat = relationship("Chat", backref="queues")
    is_active = Column(Boolean)
    greeting_message = Column(String)

class Chat(Base):
    def __repr__(self):
        return f"Chat(phone={self.phone}, name={self.name})"
    
    def __str__(self):
        return self.name

    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)
    is_contact = Column(Boolean)
    queue_id = Column(Integer, ForeignKey('queue.id'))
    queue = relationship("Queue", backref="chats")


#Model example
""" class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist = Column(String)
    
    def __init__(self)
        #usado para definir valores padrão (não tenho certeza)
    
    @property
    def name(self):
        return self._phone.format()  # exemplo de formatação
        
    def __repr__(self):
        return f"Chat(phone={self.phone}, name={self.name}, is_contact={self.is_contact})"

    def __str__(self):
        return f"{self.name} ({self.phone})"
        """