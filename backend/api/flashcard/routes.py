from fastapi import APIRouter, Request

router = APIRouter(prefix="/flashcard", tags=["flashcard"])

from services import flashcard
from core.config import Config
from schemas.deck import Deck as DeckSchema
from schemas.card import Card as CardSchema


@router.get("/decks")
def decks(request: Request):
    query_params = dict(request.query_params)
    return flashcard.get_decks(query_params)


@router.get("/deck/{deck_id}")
async def deck(deck_id: int, page: int = 1):
    """
    Get the deck details along with cards
    """
    return flashcard.get_deck_by_id(deck_id, {"page": page})


@router.get("/cards/{deck_id}")
async def cards(deck_id: int, page: int = 1):
    """
    Get the list of cards from a deck in pages
    """
    return flashcard.get_cards(deck_id, {'page': page})


@router.post("/deck")
async def save_deck(deck: DeckSchema):
    data = {"name": deck.name, "author": deck.author or Config.get("author"), "id": deck.id}
    return flashcard.save_deck(data)


@router.delete("/deck/{deck_id}")
async def delete_deck(deck_id: int, permanent: int = 0):
    # TODO, support multiple query params support
    flashcard.delete_deck(deck_id, permanent)
    return True


@router.post("/card")
async def save_card(card: CardSchema):
    data = {"deck_id": card.deck_id, "question": card.question, "answer": card.answer, "id": card.id}
    return flashcard.save_card(data)


@router.delete("/deck/{deck_id}/card/{card_id}")
async def delete_card(deck_id: int, card_id: int, permanent: int = 0):
    flashcard.delete_card(deck_id, card_id, permanent)
    return True


@router.get("/cards/due")
async def get_due():
    # TODO, finish the card due
    card_due = flashcard.get_card_due()
    return card_due


@router.post("/cards/learn")
async def learn():
    """
    Re-review the cards for review
    """
    # TODO, finish the learn
    flashcard.initiate_learning()