from pydantic import BaseModel
from enum import Enum

class Rating(Enum):
    Again = 1
    Hard = 2
    Good = 3
    Easy = 4

class CardReviewDue(BaseModel):
    card_id: int
    rating: Rating