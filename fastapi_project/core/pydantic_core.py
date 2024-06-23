from datetime import date
from typing import Optional

from pydantic import BaseModel, field_serializer, field_validator


class VoteNotInRangeError(Exception):
    def __init__(self, value, message) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class CreateOpinion(BaseModel):
    """
    Represents the data required to create an opinion.

    Attributes:
        username (str): The username of the opinion creator.
        opinion (str): The text of the opinion.
        vote (int): The vote value, ranging from 1 to 5.
        date_of_visit (Optional[date]): The date of the visit (optional).
        place_id (int): The ID of the place associated with the opinion.
    """

    username: str = "anonymous"
    opinion: str
    vote: int
    date_of_visit: Optional[date] = None
    place_id: int

    @field_validator("vote")
    @classmethod
    def is_in_range(cls, value: int):
        """
        Validates if the vote value is in the range of 1-5.

        Args:
            value (int): The vote value to validate.

        Raises:
            VoteNotInRangeError: If the vote value is not in the range of 1-5.

        Returns:
            int: The validated vote value.
        """
        if value not in [1, 2, 3, 4, 5]:
            raise VoteNotInRangeError(value, "Vote must be in range 1-5")
        return value

    @field_serializer("date_of_visit")
    @classmethod
    def serialize_date_of_visit(cls, value):
        """
        Serializes the date_of_visit field.

        Args:
            value: The value of the date_of_visit field.

        Returns:
            The serialized value of the date_of_visit field.

        Serializes the date_of_visit value to a string in the format "YYYY-MM-DD".
        """
        if value is None:
            return value

        if isinstance(value, str):
            return value

        return value.strftime("%Y-%m-%d")


class UpdateOpinion(CreateOpinion):
    """
    Represents the data required to update an opinion.
    """

    username: Optional[str] = None
    opinion: Optional[str] = None
    vote: Optional[int] = None
    date_of_visit: Optional[date] = None
    place_id: Optional[int] = None

    @field_validator("vote")
    @classmethod
    def is_in_range(cls, value: int):
        """
        Validates if the vote value is in the range of 1-5 or None.
        """
        if value not in [None, 1, 2, 3, 4, 5]:
            raise VoteNotInRangeError(value, "Vote must be in range 1-5")
        return value


class Opinion(CreateOpinion):
    """
    Represents an opinion.
    """

    id: int


class CreatePlace(BaseModel):
    """
    Represents the data required to create a place.
    """

    name: str
    description: str
    country: str
    city: Optional[str] = None
    address: Optional[str] = None


class UpdatePlace(CreatePlace):
    """
    Represents the data required to update a place.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None


class Place(CreatePlace):
    """
    Represents a place.
    """

    id: int
