from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime,func, ForeignKey
from sqlalchemy.orm import DeclarativeBase,relationship, backref
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
    coments = relationship("Coments", back_populates="like")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email= Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)
    img=Column(String(200), unique=False, nullable=True)
    description=Column(String(1000), unique=False, nullable=True)
    role = Column(String(50), nullable=True)
    created_at = Column("created_at", DateTime, default=func.now())
    ratings = relationship("Rating", back_populates="user")
    game = relationship("Game", back_populates="user")
    news = relationship("News", back_populates="user")
    coments=relationship("Coments", back_populates="user")

game_tag_association = Table(
    'game_tag_association',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

news_tag_association = Table(
    'news_tag_association',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    platforms=Column(String(100), unique=False, nullable=False)
    companys=Column(String(100), unique=False, nullable=False)
    description=Column(String(4500), unique=False, nullable=True)
    img=Column(String(350), unique=False, nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    ratings = relationship(
        "Rating", back_populates="game", cascade="all, delete-orphan"
    )
    user = relationship("User", back_populates="game")
    coments=relationship(
        "Coments", back_populates="news", cascade="all, delete-orphan"
    )
    tags = relationship('Tag', secondary=game_tag_association, backref='games')

    
class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    author=Column(String(100), unique=False, nullable=False)
    description=Column(String(5500), unique=False, nullable=True)
    img=Column(String(350), unique=False, nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    ratings = relationship(
        "Rating", back_populates="news", cascade="all, delete-orphan"
    )
    user = relationship("User", back_populates="news")
    coments=relationship(
        "Coments", back_populates="news", cascade="all, delete-orphan"
    )
    tags = relationship('Tag', secondary=news_tag_association, backref='news')

class Coments(Base):
    __tablename__ = 'coments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  
    user = relationship("User", back_populates="coments")
    content = Column(String(1500), unique=False, nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    parent_id = Column(Integer, ForeignKey('coments.id'))  
    parent = relationship("Coments", remote_side=[id])  
    like = relationship("Rating", back_populates="coments")
    children = relationship("Coments", backref=backref('parent', remote_side=[id])) 
    news_id = Column(Integer, ForeignKey("news.id"), nullable=True)
    games_id = Column(Integer, ForeignKey("games.id"), nullable=True)
    game = relationship("Game", back_populates="coments")
    news = relationship("News", back_populates="coments")

