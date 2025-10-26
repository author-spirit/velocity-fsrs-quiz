"""Applies all tables and schema"""

from datetime import datetime
import sys
import os

# Ensure parent directory is in sys.path so 'models' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import *  # Ensure you import your db instance
from models.deck import Deck
from models.card import Card

print("Creating tables")
with db:
    db.create_tables([Deck, Card])
print("Created tables")