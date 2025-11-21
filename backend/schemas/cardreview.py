from pydantic import BaseModel
from datetime import datetime

class CardReview(BaseModel):
    card_id: int
    state: int
    step: int = 1
    stability: float
    difficulty: float
    due: datetime
    last_review: datetime
