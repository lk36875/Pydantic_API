"""Unit tests for the database operations"""

from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.core.pydantic_core import CreateOpinion, CreatePlace, UpdateOpinion, UpdatePlace
from fastapi_project.repositories import OpinionRepository, PlaceRepository

"""Test the OpinionRepository"""


@pytest.fixture
def valid_opinion():
    opinion = CreateOpinion(
        place_id=1,
        username="test_user",
        opinion="test_opinion",
        vote=1,
        date_of_visit=date(2024, 1, 1),
    )
    return opinion


async def test_create_opinion(valid_opinion: CreateOpinion, db: AsyncSession):
    opinion = await OpinionRepository().create_opinion(valid_opinion, db)
    assert opinion.username == "test_user"
    assert opinion.opinion == "test_opinion"
    assert opinion.vote == 1
    assert opinion.date_of_visit == date(2024, 1, 1)


async def test_get_opinions(db: AsyncSession):
    opinions = await OpinionRepository().get_opinions(db)
    assert len(opinions) == 5


async def test_get_opinion_exists(db: AsyncSession):
    opinion = await OpinionRepository().get_opinion(1, db)
    assert opinion.username == "test_user"


async def test_invalid_opinion_id(db: AsyncSession):
    with pytest.raises(Exception):
        await OpinionRepository().get_opinion(100, db)


async def test_delete_opinion(db: AsyncSession):
    result = await OpinionRepository().delete_opinion(1, db)
    assert result == {"status": "ok"}
    remaining_opinions = await OpinionRepository().get_opinions(db)
    assert len(remaining_opinions) == 4


async def test_update_opinion(db: AsyncSession):
    updated_opinion = UpdateOpinion(
        username="test_user",
        opinion="test_opinion",
        vote=1,
        date_of_visit=date(2024, 1, 1),
    )
    opinion = await OpinionRepository().update_opinion(1, updated_opinion, db)
    assert opinion.username == "test_user"
    assert opinion.opinion == "test_opinion"
    assert opinion.vote == 1
    assert opinion.date_of_visit == date(2024, 1, 1)


@pytest.mark.parametrize(
    "username, opinion, vote, date_of_visit",
    [
        (None, None, 1, date(2024, 1, 1)),
        ("test_user", None, None, None),
        ("test_user", "test_opinion", 1, date(2024, 1, 1)),
    ],
)
async def test_valid_updates_opinion(username, opinion, vote, date_of_visit, db: AsyncSession):
    old_username = (await OpinionRepository().get_opinion(1, db)).username
    updated_opinion = UpdateOpinion(
        username=username,
        opinion=opinion,
        vote=vote,
        date_of_visit=date_of_visit,
    )
    await OpinionRepository().update_opinion(1, updated_opinion, db)
    assert (await OpinionRepository().get_opinion(1, db)).username == old_username


async def test_invalid_id_update_opinion(db: AsyncSession):
    with pytest.raises(Exception):
        await OpinionRepository().update_opinion(100, UpdateOpinion(), db)


"""Test the PlaceRepository"""


async def test_create_place(db: AsyncSession):
    place = CreatePlace(
        name="test_name",
        description="test_description",
        country="test_country",
        city="test_city",
        address="test_address",
    )
    result = await PlaceRepository().create_place(place, db)
    assert result.name == "test_name"
    assert result.description == "test_description"
    assert result.country == "test_country"
    assert result.city == "test_city"
    assert result.address == "test_address"


async def test_get_places(db: AsyncSession):
    places = await PlaceRepository().get_places(db)
    assert len(places) == 5


async def test_get_place_exists(db: AsyncSession):
    place = await PlaceRepository().get_place(1, db)
    assert place.name == "test_name"


async def test_invalid_place_id(db: AsyncSession):
    with pytest.raises(Exception):
        await PlaceRepository().get_place(100, db)


async def test_update_place(db: AsyncSession):
    updated_place = UpdatePlace(
        name="test_name",
        description="test_description",
        country="test_country",
        city="test_city",
        address="test_address",
    )
    place = await PlaceRepository().update_place(1, updated_place, db)
    assert place.name == "test_name"
    assert place.description == "test_description"
    assert place.country == "test_country"
    assert place.city == "test_city"
    assert place.address == "test_address"


async def test_invalid_id_update_place(db: AsyncSession):
    with pytest.raises(Exception):
        await PlaceRepository().update_place(100, UpdatePlace(), db)


async def test_delete_place(db: AsyncSession):
    result = await PlaceRepository().delete_place(1, db)
    assert result == {"status": "ok"}
    remaining_places = await PlaceRepository().get_places(db)
    assert len(remaining_places) == 4


async def test_invalid_id_delete_place(db: AsyncSession):
    with pytest.raises(Exception):
        await PlaceRepository().delete_place(100, db)


async def test_get_opinions_for_place(db: AsyncSession):
    opinions = await PlaceRepository().get_opinions_for_place(1, db)
    assert len(opinions) == 3
