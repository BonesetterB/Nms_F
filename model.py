from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email= Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    platforms=Column(String(100), unique=False, nullable=False)
    companys=Column(String(100), unique=False, nullable=False)
    descripthion=Column(String(100), unique=False, nullable=False)
    img=Column(String(200), unique=False, nullable=False)

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    author=Column(String(100), unique=False, nullable=False)
    descripthion=Column(String(2000), unique=False, nullable=False)
    img=Column(String(200), unique=False, nullable=False)