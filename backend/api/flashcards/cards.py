from fastapi import APIRouter, HTTPException
from services.flashcard import flashcard
from schemas.card import Card as CardSchema
from core.logs import logger

router = APIRouter(prefix="/flashcards/cards", tags=["cards"])

@router.get("/")
async def list_cards(deck_id: int, page: int = 1):
    """
    Get the list of cards from a deck in pages via query params: /cards?deck_id=1&page=1
    """
    return Flashcard.get_cards(deck_id, {'page': page})


@router.post("/")
async def save_card(card: CardSchema):
    """Create or update a card in a deck."""
    data = {
        "deck_id": card.deck_id,
        "question": card.question,
        "answer": card.answer,
    }
    try:
        return Flashcard.save_card(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/")
async def edit_card(card: CardSchema):
    """
    Update a card's question or answer by its card.id (in payload).
    """
    data = {
        "id": card.id,
        "question": card.question,
        "answer": card.answer,
        "deck_id": card.deck_id,
    }
    logger.info(data)
    return Flashcard.save_card(data)

@router.delete("/{card_id}")
async def delete_card(card_id: int):
    try:
        res: bool = Flashcard.delete_card(card_id)
        return {"deleted": res}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/trash")
async def trash_card(card_id: int):
    """
    Trash the card
    Args:
        deck_id (int): deck id of card
        card_id (int): card id to trash 
    """
    try:
        res: bool = Flashcard.trash_card(card_id)
        return {"trashed": res, "card_id": card_id}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))