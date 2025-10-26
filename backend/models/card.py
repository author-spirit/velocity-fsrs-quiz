from peewee import ForeignKeyField, TextField, PrimaryKeyField
from db.database import BaseModel
from models.deck import Deck

class Card(BaseModel):
    deck = ForeignKeyField(Deck, backref='cards')
    question = TextField()
    answer = TextField()

    def to_dict(self):
        return {}