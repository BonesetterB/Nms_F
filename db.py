import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase,sessionmaker

from config import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: sessionmaker | None = sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self._engine, class_=AsyncSession
        )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncSession:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.sqlalchemy_database_url)


async def get_db() -> AsyncSession:
    async with sessionmanager.session() as session:
        return session