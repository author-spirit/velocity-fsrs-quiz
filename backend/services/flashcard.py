from core.logs import logger
from models.card import Card
from models.deck import Deck
from models.cardreview import CardReview
from datetime import datetime
from typing import Union
import json
from playhouse.shortcuts import model_to_dict
from services.spacedrepetition import SpacedRepetition
from utils import helpers

PAGE_LIMIT = 10

def save_deck(data: dict) -> dict:
    """
    Saves a deck to the database. If 'id' is not present in data, creates a new deck.
    If 'id' is present, updates the existing deck with new information.

    Args:
        data (dict): Dictionary containing deck details such as 'id', 'name', and 'author'.

    Returns:
        dict: The saved deck as a dictionary.
    """

    if not data.get("id"):
        deck = Deck(
            name=data.get("name"),
            author=data.get("author"),
            createdtime=datetime.now(),
            modifiedtime=datetime.now(),
        )
        deck.save()
    else:
        deck = Deck.get_or_none(data.get("id"))
        if not deck:
            raise ValueError(f"Deck with id '{data.get('id')}' does not exist.")
        updated = False
        if "name" in data and deck.name != data["name"]:
            deck.name = data["name"]
            updated = True
        if "author" in data and deck.author != data["author"]:
            deck.author = data["author"]
            updated = True
        if updated:
            deck.modifiedtime = datetime.now()
            deck.save()

    return model_to_dict(deck)


def get_deck_by_id(id: int, filters: dict) -> dict:
    """Get the deck by id along with cards
    Args:
        id (int): Deck ID
    Returns:
        Deck Instance
    """
    if not id:
        return {}

    if not filters:
        filters = {"page": 1}

    try:
        deck_obj = Deck.get_or_none(id)
        if not deck_obj:
            return {}
        deck_dict = model_to_dict(deck_obj)

        # Get all cards for this deck
        deck_dict["cards"] = get_cards(id, filters)
        return deck_dict
    except Exception as e:
        logger.error(e)
        return {}


def get_decks(filters: Union[dict, str] = None) -> Union[dict, list]:
    """
    Get all decks
    Returns:
        List of decks
    """
    # Apply pagination if 'page' is in filters; otherwise return all decks
    query = Deck.select()

    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            pass

    if not filters or not isinstance(filters, dict):
        filters = {"page": 1}

    page = int(filters.get("page", 1))
    offset = (page - 1) * PAGE_LIMIT

    # Allow only deleted, otherwise all
    deleted_filter = filters.get("deleted")
    if deleted_filter is None or str(deleted_filter).lower() == "false":
        query = query.where(Deck.is_trash == False)

    query = query.limit(PAGE_LIMIT).offset(offset)
    return [model_to_dict(deck) for deck in query]


def save_card(card_info: dict) -> dict:
    """
    Save a card information having question and answer
    Args:
        card_info (dict): A dictionary containing card details.
            For creation: should include 'deck' (deck id or Deck instance), 'question', 'answer'.
            For update: should include 'id' (card id to update), and optional 'question', 'answer'.

    Returns:
        Card instance or number of rows updated (on update).
    """
    # TODO, simplify the save
    if not card_info.get("id"):
        deck_id = card_info.get("deck_id")
        if not deck_id:
            logger.info("Deck not provided")
            raise Exception(status_code=404, detail="Deck not provided")

        card = Card(
            question=card_info.get("question"), answer=card_info.get("answer"), deck=deck_id
        )
        card.save()

    else:
        card = Card.get_or_none(card_info.get("id"))
        if not card:
            raise ValueError(f"Card with id '{card_info.get('id')}' does not exist.")
        updated = False
        if "question" in card_info and card.question != card_info.get("question"):
            card.question = card_info["question"]
            updated = True
        if "answer" in card_info and card.answer != card_info.get("answer"):
            card.answer = card_info["answer"]
            updated = True
        if updated:
            card.modifiedtime = datetime.now()
            card.save()
    return model_to_dict(card, recurse=False)


def get_cards(deck_id: int, filters: Union[dict | str]) -> list:
    """Get Cards belongs to deck
    Args:
        deck_id (int): Deck ID
        page_no (int): Page number (optional)
    Return:
        List of Cards
    """
    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            pass

    if not filters:
        filters = {"page": 1}

    query = Card.select()
    page = int(filters.get("page", 1))
    offset = (page - 1) * PAGE_LIMIT
    query = query.where(Card.deck == deck_id).limit(PAGE_LIMIT).offset(offset)
    return [model_to_dict(card, recurse=False) for card in query]


def delete_deck(deck_id: int):
    """
    Delete a deck by its ID.

    Args:
        deck_id (int): The ID of the deck to delete.
    Returns:
        int: Number of rows deleted (for hard delete), or 1 for soft delete.
    """

    # TODO, check deck_in_use
    try:
        num_deleted = Deck.delete().where(Deck.id == deck_id).execute()
        if num_deleted == 0:
            raise ValueError(f"Deck Id '{deck_id}' does not exist.")
        return True
    except ValueError:
        raise
    except Exception as e:
        logger.error(e)
        raise RuntimeError("Failed to delete deck") from e

def trash_deck(deck_id) -> bool:
    """
    Mark the deck as trashed (set is_trash to True).
    """

    # TODO, check deck_in_use
    try:
        deck = Deck.get_or_none(Deck.id == deck_id)
        if not deck:
            raise ValueError(f"Deck Id '{deck_id}' does not exist.")
        deck.is_trash = True
        deck.modifiedtime = datetime.now()
        deck.save()
        return True
    except ValueError:
        raise
    except Exception as e:
        logger.error(e)
        raise RuntimeError("Failed to trash deck") from e


def delete_card(card_id: int) -> bool:
    """
    Delete a card by its ID.

    Args:
        card_id (int): The ID of the card to delete.

    Returns:
        bool: True if the card was deleted, False otherwise.

    Raises:
        ValueError: If the card with the given ID does not exist.
        RuntimeError: If an error occurs during deletion.
    """
    try:
        num_deleted = Card.delete().where(Card.id == card_id).execute()
        if num_deleted == 0:
            raise ValueError(f"Card Id '{card_id}' does not exist.")
        return True
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("Failed to delete card") from e


def trash_card(card_id: int) -> bool:
    """
    Mark the card as trashed (set is_trash to True) by card_id in a deck.
    Args:
        card_id (int): The ID of the card to trash.
    Returns:
        int: 1 if successful, raises Exception otherwise.
    Raises:
        ValueError: If the card with the given ID does not exist.
        RuntimeError: If an error occurs during trash.
    """
    try:
        # TODO, DeckId not required  & (Card.deck == deck_id) ??
        card = Card.get_or_none(Card.id == card_id)
        if not card:
            raise ValueError(f"Card Id '{card_id}' does not exist.")
        card.is_trash = True
        card.modifiedtime = datetime.now()
        card.save()
        return True
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("Failed to trash card") from e


def get_due_cards(filters: Union[dict, str]):
    """
    List out all the cards that are due
    """

    if isinstance(filters, str):
        filters = helpers.safe_json_parse(filters)
        filters = filters or {}
    
    page = int(filters.get("page", 1))
    offset: int = (page - 1) * PAGE_LIMIT

    query = CardReview.select()

    if "deck_id" in filters:
        deck_id = filters.get("deck_id")
        query = query.join(Card).where(Card.deck == deck_id)

    due_cards = query.where(CardReview.due <= datetime.now()).limit(PAGE_LIMIT).offset(offset)
    return [model_to_dict(card, recurse=False) for card in due_cards]

def get_next_due(card_id: int, user_rating: int):
    """
    Get the due of given card
    Args:
        card_id (int): Card Id
        difficulty (int): card difficulty
            - 1: Very Hard
            - 2: Hard
            - 3: Good
            - 4: Easy
    Returns:
        dict: Next Due information of reviewed card
    """
    # Check if CardReview exists
    sr = SpacedRepetition()
    result = sr.get_next_due(card_id, user_rating)

    return result


