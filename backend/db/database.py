from peewee import Model, SqliteDatabase

db = SqliteDatabase("db/velocity.db", pragmas={'journal_mode': 'wal'})

class BaseModel(Model):
    class Meta:
        database = db


def connect():
    db.connect()

def disconnect():
    db.close()