from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_project.core.pydantic_core import CreateOpinion, CreatePlace, Opinion, Place, UpdateOpinion, UpdatePlace
from fastapi_project.core.sqlalchemy_core import DBOpinion, DBPlace

__all__ = ["NotFoundError", "OpinionRepository", "PlaceRepository"]


class NotFoundError(Exception):
    """Exception raised when an item is not found."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class OpinionRepository:
    """
    Repository class for managing opinions in the database.
    """

    async def create_opinion(self, opinion: CreateOpinion, db: AsyncSession):
        """
        Create a new opinion in the database.

        Args:
            opinion (CreateOpinion): The opinion data to be created.
            db (Session): The database session.

        Returns:
            Opinion: The created opinion.
        """
        db_opinion = DBOpinion(**opinion.__dict__)
        db.add(db_opinion)
        await db.commit()
        await db.refresh(db_opinion)
        return Opinion(**db_opinion.__dict__)

    async def get_opinions(self, db: AsyncSession):
        """
        Get all opinions from the database.

        Args:
            db (Session): The database session.

        Returns:
            dict: A dictionary of opinions, where the key is the opinion ID and the value is the opinion object.
        """
        stmt = select(DBOpinion)
        opinion_results = await db.scalars(stmt)
        opinions = opinion_results.all()
        opinions_pydantic = [Opinion(**opinion.__dict__) for opinion in opinions]
        return {opinion.id: opinion for opinion in opinions_pydantic}

    async def get_opinion(self, opinion_id: int, db: AsyncSession):
        """
        Get a specific opinion from the database.

        Args:
            opinion_id (int): The ID of the opinion to retrieve.
            db (Session): The database session.

        Returns:
            Opinion: The retrieved opinion.

        Raises:
            NotFoundError: If the opinion with the specified ID is not found.
        """
        stmt = select(DBOpinion).filter(DBOpinion.id == opinion_id)
        opinion_result = await db.scalars(stmt)
        opinion = opinion_result.first()
        if opinion is None:
            raise NotFoundError("Opinion not found")
        return Opinion(**opinion.__dict__)

    async def delete_opinion(self, opinion_id: int, db: AsyncSession):
        """
        Delete a specific opinion from the database.

        Args:
            opinion_id (int): The ID of the opinion to delete.
            db (Session): The database session.

        Returns:
            dict: A dictionary indicating the status of the deletion.

        Raises:
            NotFoundError: If the opinion with the specified ID is not found.
        """
        stmt = select(DBOpinion).filter(DBOpinion.id == opinion_id)
        opinion_result = await db.scalars(stmt)
        opinion = opinion_result.first()
        if opinion is None:
            raise NotFoundError("Opinion not found")
        await db.delete(opinion)
        await db.commit()
        return {"status": "ok"}

    async def update_opinion(self, opinion_id: int, opinion: UpdateOpinion, db: AsyncSession):
        """
        Update a specific opinion in the database.

        Args:
            opinion_id (int): The ID of the opinion to update.
            opinion (UpdateOpinion): The updated opinion data.
            db (Session): The database session.

        Returns:
            Opinion: The updated opinion.

        Raises:
            NotFoundError: If the opinion with the specified ID is not found.
        """
        stmt = select(DBOpinion).filter(DBOpinion.id == opinion_id)
        db_opinion_result = await db.scalars(stmt)
        db_opinion = db_opinion_result.first()
        if db_opinion is None:
            raise NotFoundError("Opinion not found")
        for key, value in opinion.__dict__.items():
            if value is not None:
                setattr(db_opinion, key, value)
        await db.commit()
        await db.refresh(db_opinion)
        return Opinion(**db_opinion.__dict__)


class PlaceRepository:
    """
    Repository class for managing places in the database.
    """

    async def create_place(self, place: CreatePlace, db: AsyncSession):
        """
        Create a new place in the database.

        Args:
            place (CreatePlace): The place data to be created.
            db (Session): The database session.

        Returns:
            Place: The created place.
        """
        db_place = DBPlace(**place.__dict__)
        db.add(db_place)
        await db.commit()
        await db.refresh(db_place)
        return Place(**db_place.__dict__)

    async def get_places(self, db: AsyncSession):
        """
        Get all places from the database.

        Args:
            db (Session): The database session.

        Returns:
            dict: A dictionary of places, where the keys are the place IDs and the values are the places.
        """
        stmt = select(DBPlace)
        place_results = await db.scalars(stmt)
        places = place_results.all()
        places_pydantic = [Place(**place.__dict__) for place in places]
        return {place.id: place for place in places_pydantic}

    async def get_place(self, place_id: int, db: AsyncSession):
        """
        Get a specific place from the database.

        Args:
            place_id (int): The ID of the place to retrieve.
            db (Session): The database session.

        Returns:
            Place: The retrieved place.

        Raises:
            NotFoundError: If the place with the given ID is not found.
        """
        stmt = select(DBPlace).filter(DBPlace.id == place_id)
        place_result = await db.scalars(stmt)
        place = place_result.first()
        if place is None:
            raise NotFoundError("Place not found")
        return Place(**place.__dict__)

    async def delete_place(self, place_id: int, db: AsyncSession):
        """
        Delete a specific place from the database.

        Args:
            place_id (int): The ID of the place to delete.
            db (Session): The database session.

        Returns:
            dict: A dictionary indicating the status of the deletion.

        Raises:
            NotFoundError: If the place with the given ID is not found.
        """
        stmt = select(DBPlace).filter(DBPlace.id == place_id)
        place_result = await db.scalars(stmt)
        place = place_result.first()
        if place is None:
            raise NotFoundError("Place not found")
        await db.delete(place)
        await db.commit()
        return {"status": "ok"}

    async def update_place(self, place_id: int, place: UpdatePlace, db: AsyncSession):
        """
        Update a specific place in the database.

        Args:
            place_id (int): The ID of the place to update.
            place (UpdatePlace): The updated place data.
            db (Session): The database session.

        Returns:
            Place: The updated place.

        Raises:
            NotFoundError: If the place with the given ID is not found.
        """
        stmt = select(DBPlace).filter(DBPlace.id == place_id)
        db_place_result = await db.scalars(stmt)
        db_place = db_place_result.first()
        if db_place is None:
            raise NotFoundError("Place not found")
        for key, value in place.__dict__.items():
            if value is not None:
                setattr(db_place, key, value)
        await db.commit()
        await db.refresh(db_place)
        return Place(**db_place.__dict__)

    async def get_opinions_for_place(self, place_id: int, db: AsyncSession):
        """
        Get the opinions for a specific place from the database.

        Args:
            place_id (int): The ID of the place to retrieve opinions for.
            db (Session): The database session.

        Returns:
            List[Opinion]: The opinions for the place.

        Raises:
            NotFoundError: If the place with the given ID is not found.
        """
        stmt = select(DBPlace).filter(DBPlace.id == place_id).options(selectinload(DBPlace.opinions))
        place_result = await db.scalars(stmt)
        place = place_result.first()
        if place is None:
            raise NotFoundError("Place not found")
        return place.opinions
