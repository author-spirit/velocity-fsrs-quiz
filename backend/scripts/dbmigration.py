import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.database import *
from playhouse.migrate import *
from datetime import datetime
from models.cardreview import CardReview

connect()

def safe_add_column(table, column, field):
    cols = [c.name for c in db.get_columns(table)]
    if column not in cols:
        migrate(migrator.add_column(table, column, field))
        print(f"'{column}' column successfully added to {table}")


migrator = SqliteMigrator(db)

if not CardReview.table_exists():
    db.create_tables([CardReview])
    print("CardReview table created")

# Deck Fields
safe_add_column('deck', 'is_trash', BooleanField(default=False)),
    
# Card Fields
safe_add_column('card', 'createdtime', DateTimeField(default=datetime.now)),
safe_add_column('card', 'modifiedtime', DateTimeField(null=True))
safe_add_column('card', 'is_trash', BooleanField(default=False))

# review
safe_add_column("cardreview", 'step', IntegerField(null=True))

# TODO, move to ambelic?? something

disconnect()