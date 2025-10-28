import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.database import *
from playhouse.migrate import *
from datetime import datetime

connect()

def safe_add_column(table, column, field):
    cols = [c.name for c in db.get_columns(table)]
    if column not in cols:
        migrate(migrator.add_column(table, column, field))

migrator = SqliteMigrator(db)

# Deck Fields
safe_add_column('deck', 'is_trash', BooleanField(default=False)),
    
# Card Fields
safe_add_column('card', 'createdtime', DateTimeField(default=datetime.now)),
safe_add_column('card', 'modifiedtime', DateTimeField(null=True))

disconnect()