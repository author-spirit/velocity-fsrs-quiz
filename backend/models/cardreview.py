from peewee import ForeignKeyField, DateTimeField, FloatField, IntegerField
from db.database import BaseModel
from models.card import Card

"""
About the fields:
state: 0 = New, 1 = Learning/Relearning, 2 = Review
step: Learning step number (1,2,3…) when state = 1, None when state = 2
stability: Memory retention duration in days (higher = longer interval)
difficulty: Card hardness score (~1–10 scale, updated by ratings)
due: Next scheduled review timestamp
last_review: Previous reviewed timestamp

Doubts: 
https://github.com/open-spaced-repetition/fsrs4anki/blob/main/docs/tutorial.md
"""

class CardReview(BaseModel):
    card = ForeignKeyField(Card, backref='card_review')
    state = IntegerField()
    step = IntegerField(null=True)         
    stability = FloatField()
    difficulty = FloatField()
    due = DateTimeField()
    last_review = DateTimeField()