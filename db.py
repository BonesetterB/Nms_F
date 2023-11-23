from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlite3 import Error
from config import Settings




db = create_engine(Settings.sqlalchemy_database_url, echo=True)
Session = sessionmaker(bind=db)
session = Session()