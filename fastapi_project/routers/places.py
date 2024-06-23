from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.core.pydantic_core import CreatePlace, Opinion, Place, UpdatePlace
from fastapi_project.db.create_db import get_db
from fastapi_project.repositories import NotFoundError, PlaceRepository

router = APIRouter(
    prefix="/places",
    tags=["places"],
    responses={404: {"description": "Not found"}},
)


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
def health_check():
    """Health check for the places router."""
    return {"status": "ok"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_places(db: AsyncSession = Depends(get_db)):
    """Get all places from the database."""
    places = await PlaceRepository().get_places(db)
    return places


@router.get("/{place_id}", status_code=status.HTTP_200_OK)
async def get_place(place_id: int, db: AsyncSession = Depends(get_db)):
    """Get a place by its ID."""
    try:
        place = await PlaceRepository().get_place(place_id, db)
        return Place(**place.__dict__)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_place(place: CreatePlace, db: AsyncSession = Depends(get_db)):
    """Create a new place."""
    db_place = await PlaceRepository().create_place(place, db)
    return Place(**db_place.__dict__)


@router.delete("/{place_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_place(place_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a place by its ID."""
    try:
        result = await PlaceRepository().delete_place(place_id, db)
        return result
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")


@router.put("/{place_id}", status_code=status.HTTP_200_OK)
async def update_place(place_id: int, place: UpdatePlace, db: AsyncSession = Depends(get_db)):
    """Update specified fields of a place by its ID."""
    try:
        db_place = await PlaceRepository().update_place(place_id, place, db)
        return Place(**db_place.__dict__)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")


@router.get("/{place_id}/opinions", status_code=status.HTTP_200_OK)
async def get_opinions_for_place(place_id: int, db: AsyncSession = Depends(get_db)):
    """Get all opinions for a place by its ID."""
    opinions = await PlaceRepository().get_opinions_for_place(place_id, db)
    return [Opinion(**opinion.__dict__) for opinion in opinions]
