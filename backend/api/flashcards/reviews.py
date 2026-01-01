from schemas.cardreviewdue import CardReviewDue
from core.logs import logger
from fastapi import APIRouter, Body, HTTPException
from services import flashcard

router = APIRouter(prefix="/flashcards/reviews", tags=["reviews"])

@router.get("/due")
async def get_due_cards(page: int = None):
    page = page or 1
    card_due = flashcard.get_due_cards({"page": page})
    return card_due

@router.post("/")
async def review_card(carddue: CardReviewDue):
    """
    Learn a card for the first time, optionally with an initial rating.
    """
    print("card review", carddue.rating)
    result = flashcard.get_next_due(carddue.card_id, carddue.rating)
    if result.get("error"):
        logger.error(result['error'])
        raise HTTPException(status_code=400, detail=result["error"])
    return result

