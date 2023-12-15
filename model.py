from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime,func, ForeignKey
from sqlalchemy.orm import DeclarativeBase,relationship
from datetime import date

class Base(DeclarativeBase):
    pass

class Role():


    user: str = "User"
    moder: str = "Moderator"
    admin: str = "Administrator"

class Rating(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)
    news_id = Column(Integer, ForeignKey("news.id"), nullable=True)
    games_id = Column(Integer, ForeignKey("games.id"), nullable=True)

    user = relationship("User", back_populates="ratings")
    game = relationship("Game", back_populates="ratings")
    news = relationship("News", back_populates="ratings")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email= Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)
    img=Column(String(200), unique=False, nullable=True)
    role = Column(String(50), nullable=True)
    created_at = Column("created_at", DateTime, default=func.now())
    ratings = relationship("Rating", back_populates="user")




class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    platforms=Column(String(100), unique=False, nullable=False)
    companys=Column(String(100), unique=False, nullable=False)
    descripthion=Column(String(1500), unique=False, nullable=False)
    img=Column(String(200), unique=False, nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    ratings = relationship(
        "Rating", back_populates="game", cascade="all, delete-orphan"
    )

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    author=Column(String(100), unique=False, nullable=False)
    descripthion=Column(String(2000), unique=False, nullable=False)
    img=Column(String(200), unique=False, nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    ratings = relationship(
        "Rating", back_populates="news", cascade="all, delete-orphan"
    )