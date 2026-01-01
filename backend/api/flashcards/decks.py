from fastapi import APIRouter, Request, HTTPException
from services import flashcard
from core.config import Config
from schemas.deck import Deck as DeckSchema
from core.logs import logger

router = APIRouter(prefix="/flashcards/decks", tags=["decks"])

@router.get("/")
def list_decks(request: Request):
    query_params = dict(request.query_params)
    return flashcard.get_decks(query_params)

@router.post("/")
async def save_deck(deck: DeckSchema):
    try:
        data = {
            "name": deck.name,
            "author": deck.author or Config.get("author", "unknown"),
            "id": deck.id,
        }
        return flashcard.save_deck(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/{deck_id}")
async def get_deck(deck_id: int, page: int = 1):
    """
    Get the deck details along with cards
    """
    return flashcard.get_deck_by_id(deck_id, {"page": page})

@router.patch("/{deck_id}")
async def edit_deck(deck_id: int, deck: DeckSchema):
    data = {
        "id": deck_id,
        "name": deck.name,
        "author": deck.author or Config.get("author", "unknown"),
    }
    return flashcard.save_deck(data)

@router.delete("/{deck_id}")
async def delete_deck(deck_id: int):
    try:
        res: bool = flashcard.delete_deck(deck_id)
        return {"deleted": res}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{deck_id}/trash")
async def trash_deck(deck_id: int):
    try:
        res: bool = flashcard.trash_deck(deck_id)
        return {"trashed": res, "deck_id": deck_id}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))
