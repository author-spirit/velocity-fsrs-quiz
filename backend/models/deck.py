from peewee import CharField, DateTimeField, PrimaryKeyField
from db.database import BaseModel
from datetime import datetime

class Deck(BaseModel):
    name = CharField(unique=True)
    author = CharField()
    createdtime = DateTimeField(default=datetime.now)
    modifiedtime = DateTimeField()

    def to_dict(self):
        return {
            'name': self.name,
            'author': self.author,
            'createdtime': self.createdtime,
            'modifiedtime': self.modifiedtime,
        }