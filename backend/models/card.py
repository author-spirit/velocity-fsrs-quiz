from peewee import ForeignKeyField, TextField, DateTimeField
from db.database import BaseModel
from datetime import datetime
from models.deck import Deck

class Card(BaseModel):
    deck = ForeignKeyField(Deck, backref='cards')
    question = TextField()
    answer = TextField()
    # createdtime = DateTimeField(default=datetime.now)
    # modifiedtime = DateTimeField()

    def to_dict(self):
        return {}