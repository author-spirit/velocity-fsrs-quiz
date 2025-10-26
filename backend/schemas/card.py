from pydantic import BaseModel
# from schemas.deck import Deck
class Card(BaseModel):
    deck_id: int
    question: str
    answer: str