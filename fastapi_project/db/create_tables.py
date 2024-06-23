import os
import asyncio
from datetime import date

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from fastapi_project.app import app
from fastapi_project.core.sqlalchemy_core import Base, DBOpinion, DBPlace

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///dev.db")
ENGINE: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE, class_=AsyncSession)


async def example_data(session: AsyncSession):
    """
    Insert example data into the database.

    Args:
        session: The database session.

    Returns:
        None
    """
    opinion_data = [
        {
            "username": "john_doe",
            "opinion": "Great place with excellent service!",
            "vote": 5,
            "date_of_visit": date(2023, 5, 15),
            "place_id": 1,
        },
        {
            "username": "alice_smith",
            "opinion": "The food was delicious, but the atmosphere could be improved.",
            "vote": 4,
            "date_of_visit": date(2023, 7, 2),
            "place_id": 2,
        },
        {
            "username": "bob_jones",
            "opinion": "Not impressed, won't be coming back.",
            "vote": 2,
            "date_of_visit": date(2023, 8, 20),
            "place_id": 3,
        },
    ]

    place_data = [
        {
            "name": "The Gourmet Kitchen",
            "description": "A fine dining experience with a diverse menu.",
            "country": "United States",
            "city": "New York",
            "address": "123 Main St",
        },
        {
            "name": "Cozy Cafe",
            "description": "Quaint cafe serving a variety of coffee and pastries.",
            "country": "United Kingdom",
            "city": "London",
            "address": "456 Oak St",
        },
        {
            "name": "Fast & Fresh Bistro",
            "description": "Quick-service bistro with a focus on fresh ingredients.",
            "country": "Canada",
            "city": "Toronto",
            "address": "789 Maple St",
        },
    ]

    for place in place_data:
        new_place = DBPlace(**place)
        session.add(new_place)

    for opinion in opinion_data:
        new_opinion = DBOpinion(**opinion)
        session.add(new_opinion)

    await session.commit()


async def create_all():
    """Create the database and example data."""
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SESSION_LOCAL() as session:  # type: ignore
        await example_data(session)


if __name__ == "__main__":
    asyncio.run(create_all())
