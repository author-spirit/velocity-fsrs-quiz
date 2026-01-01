from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Deck(BaseModel):
    id: Optional[int] = None
    name: str
    author: Optional[str] = None