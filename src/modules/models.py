from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#Model example
""" class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist = Column(String) """