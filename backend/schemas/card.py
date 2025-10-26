from optparse import Option
from pydantic import BaseModel
from typing import Optional

class Card(BaseModel):
    id: Optional[int] = None
    deck_id: Optional[int] = None
    question: Optional[str] = None
    answer: Optional[str] = None