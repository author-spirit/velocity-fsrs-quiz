from peewee import ForeignKeyField, DateTimeField, FloatField, IntegerField
from db.database import BaseModel
from models.card import Card

# About the fields
# state: 0=NewCard; 1=Learning; 2=Review (stabilizing long term)
# step: learning step, 0, 1,2 etc
# stability: how long memory lasts
# difficulty: (Again/Hard/Good/Easy) just like in anki
# due: next card review timestamp.
# last_review: Timestamp of the previously reviewed card.

class CardReview(BaseModel):
    card = ForeignKeyField(Card, backref='card_review')
    state = IntegerField()
    step = IntegerField(default=1)         
    stability = FloatField()
    difficulty = FloatField()
    due = DateTimeField()
    last_review = DateTimeField()