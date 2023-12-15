from config import settings
import asyncpg

async def connect_to_db():
    conn = await asyncpg.connect(
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_db,
        host=settings.postgres_host
    )
    return conn
