from peewee import BooleanField, CharField, DateTimeField
from db.database import BaseModel
from datetime import datetime

class Deck(BaseModel):
    name = CharField(unique=True)
    author = CharField()
    createdtime = DateTimeField(default=datetime.now)
    modifiedtime = DateTimeField()
    is_trash = BooleanField(default=False)