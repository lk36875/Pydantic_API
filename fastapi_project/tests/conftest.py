from contextlib import asynccontextmanager

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_project.app import app
from fastapi_project.core.sqlalchemy_core import Base, DBOpinion, DBPlace
from fastapi_project.db.create_db import get_db


@asynccontextmanager
async def local_session():
    """
    Context manager provides a local session for testing purposes.
    It creates an in-memory SQLite database and initializes it with test data.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as db:
        opinions = [
            DBOpinion(id=1, username="test_user", opinion="test_opinion", vote=1, place_id=1),
            DBOpinion(id=2, username="test_user2", opinion="test_opinion2", vote=2, place_id=2),
            DBOpinion(id=3, username="test_user3", opinion="test_opinion3", vote=3, place_id=1),
            DBOpinion(id=4, username="test_user4", opinion="test_opinion4", vote=4, place_id=1),
            DBOpinion(id=5, username="test_user5", opinion="test_opinion5", vote=5, place_id=2),
        ]
        db.add_all(opinions)

        places = [
            DBPlace(
                id=1,
                name="test_name",
                description="test_description",
                country="test_country",
                city="test_city",
                address="test_address",
            ),
            DBPlace(
                id=2,
                name="test_name2",
                description="test_description2",
                country="test_country2",
                city="test_city2",
                address="test_address2",
            ),
            DBPlace(
                id=3,
                name="test_name3",
                description="test_description3",
                country="test_country3",
                city="test_city3",
                address="test_address3",
            ),
            DBPlace(
                id=4,
                name="test_name4",
                description="test_description4",
                country="test_country4",
                city="test_city4",
                address="test_address4",
            ),
            DBPlace(
                id=5,
                name="test_name5",
                description="test_description5",
                country="test_country5",
                city="test_city5",
                address="test_address5",
            ),
        ]
        db.add_all(places)

        await db.commit()
        try:
            yield db
        finally:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client():
    """
    TestClient instance for testing the FastAPI app.
    It overrides the get_db dependency to use a local session for testing purposes.
    """
    async with TestClient(app) as client:

        async def _override_get_db():
            async with local_session() as database:
                yield database

        app.dependency_overrides[get_db] = _override_get_db
        yield client
        app.dependency_overrides = {}


@pytest.fixture(scope="function")
async def db():
    """
    Local session for testing purposes.
    """
    async with local_session() as database:
        yield database
