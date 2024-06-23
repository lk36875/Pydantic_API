import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///dev.db")
engine = create_async_engine(DATABASE_URL)
session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    """
    Get a database session.

    Returns:
        Database session object.
    """
    database = session_local()
    try:
        yield database
    finally:
        await database.close()
