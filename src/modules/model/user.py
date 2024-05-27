from ..database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
    
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", backref="books")

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, author={self.author})"