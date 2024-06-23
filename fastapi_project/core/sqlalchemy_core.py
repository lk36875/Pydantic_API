from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DBOpinion(Base):
    """
    Represents an opinion in the database.

    Attributes:
        id (int): The unique identifier of the opinion.
        username (str): The username of the user who provided the opinion.
        opinion (str, optional): The text of the opinion.
        vote (int): The vote associated with the opinion.
        date_of_visit (date, optional): The date of the visit associated with the opinion.
        place_id (int): The ID of the place associated with the opinion.
        place (DBPlace): The place associated with the opinion.

    Methods:
        __repr__(): Returns a string representation of the DBOpinion object.
    """

    __tablename__ = "opinions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    opinion: Mapped[Optional[str]]
    vote: Mapped[int]
    date_of_visit: Mapped[Optional[date]]
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id"))

    place = relationship("DBPlace", back_populates="opinions")

    def __repr__(self):
        return (
            f"<DBOpinion(username={self.username}, opinion={self.opinion}, "
            f"vote={self.vote}, date_of_visit={self.date_of_visit})>"
        )


class DBPlace(Base):
    """
    Represents a place in the database.

    Attributes:
        id (int): The unique identifier of the place.
        name (str): The name of the place.
        description (str): The description of the place.
        country (str): The country where the place is located.
        city (str): The city where the place is located.
        address (str): The address of the place.
        opinions (list): The opinions associated with the place.
    """

    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]

    opinions = relationship("DBOpinion", back_populates="place", cascade="all, delete")

    def __repr__(self):
        return (
            f"<DBPlace(name={self.name}, description={self.description}, "
            f"country={self.country}, city={self.city}, address={self.address})>"
        )
