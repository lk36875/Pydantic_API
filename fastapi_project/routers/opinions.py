from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.core.pydantic_core import CreateOpinion, Opinion, UpdateOpinion
from fastapi_project.db.create_db import get_db
from fastapi_project.repositories import NotFoundError, OpinionRepository

router = APIRouter(
    prefix="/opinions",
    tags=["opinions"],
    responses={404: {"description": "Not found"}},
)

router.get("/healthcheck")


def health_check():
    return {"status": "ok"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_opinions(db: AsyncSession = Depends(get_db)):
    """Get all opinions from the database."""
    opinions = await OpinionRepository().get_opinions(db)
    return opinions


@router.get("/{opinion_id}", status_code=status.HTTP_200_OK)
async def get_opinion(opinion_id: int, db: AsyncSession = Depends(get_db)):
    """Get an opinion by its ID."""
    try:
        opinion = await OpinionRepository().get_opinion(opinion_id, db)
        return Opinion(**opinion.__dict__)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opinion not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_opinion(opinion: CreateOpinion, db: AsyncSession = Depends(get_db)):
    """Create a new opinion."""
    db_opinion = await OpinionRepository().create_opinion(opinion, db)
    return Opinion(**db_opinion.__dict__)


@router.delete("/{opinion_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_opinion(opinion_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an opinion by its ID."""
    try:
        result = await OpinionRepository().delete_opinion(opinion_id, db)
        return result
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opinion not found")


@router.put("/{opinion_id}", status_code=status.HTTP_200_OK)
async def update_opinion(opinion_id: int, opinion: UpdateOpinion, db: AsyncSession = Depends(get_db)):
    """Update specified fields of an opinion by its ID."""
    try:
        db_opinion = await OpinionRepository().update_opinion(opinion_id, opinion, db)
        return Opinion(**db_opinion.__dict__)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opinion not found")
