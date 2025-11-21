from models.card import Card
from models.deck import Deck
from datetime import datetime
from db.database import *
from typing import Optional, Union
import json
from playhouse.shortcuts import model_to_dict

PAGE_LIMIT = 10

def save_deck(data: dict) -> None:
    """
    Saves a deck to the database. If 'id' is not present in data, creates a new deck.
    If 'id' is present, updates the existing deck with new information.

    Args:
        data (dict): Dictionary containing deck details such as 'id', 'name', and 'author'.

    Returns:
        dict: The saved deck as a dictionary.
    """

    # TODO, Give option for creating cards via API
    if not data.get("id"):
        deck = Deck(
            name=data.get("name"),
            author=data.get("author"),
            createdtime=datetime.now(),
            modifiedtime=datetime.now(),
        )
        deck.save()
    else:
        deck = Deck.get_or_none(Deck._meta.primary_key == data.get("id"))
        if deck:
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
        deck_obj = Deck.get_or_none(Deck.id == id)
        if not deck_obj:
            return {}
        deck_dict = model_to_dict(deck_obj)

        # Get all cards for this deck
        deck_dict["cards"] = get_cards(id, filters)
        return deck_dict
    except Exception as e:
        print(e)
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

    if not filters:
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
            raise Exception(status_code=404, detail="Deck not provided")

        card = Card(
            question=card_info.get("question"), answer=card_info.get("answer"), deck=deck_id
        )
        card.save()

    else:
        card = Card.get_or_none(Card._meta.primary_key == card_info.get("id"))
        if card:
            updated = False
            if "question" in card_info and card.question != card_info["question"]:
                card.question = card["question"]
                updated = True
            if "answer" in card_info and card.answer != card_info["answer"]:
                card.answer = card_info["answer"]
                updated = True
            if updated:
                card.modifiedtime = datetime.now()
                card.save()
    return model_to_dict(card)


def get_cards(deck_id: int, filters: Union[dict | str]) -> dict:
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
    return [model_to_dict(deck) for deck in query]


def delete_deck(deck_id, permanent: int):
    """
    Delete a deck by its ID.

    Args:
        deck_id (int): The ID of the deck to delete.
        permanent (int): If 1, perform a hard delete (permanently remove the deck from the database).
                        If 0, perform a soft delete (update the modified time but keep the deck).

    Returns:
        int: Number of rows deleted (for hard delete), or 1 for soft delete.
    """

    # TODO, If # of cards available then do not allow to delete
    try:
        deck = Deck.get_or_none(Deck.id == deck_id)
        if not deck:
            raise Exception("Deck not found")
        if permanent == 1:
            # Hard delete
            num_deleted = Deck.delete().where(Deck.id == deck_id).execute()
            return num_deleted
        else:
            # TODO, Test newly added trash field
            deck.is_trash = 1
            deck.modifiedtime = datetime.now()  # This just marks modification, not real trash delete
            deck.save()
            return 1
    except Exception as e:
        print(e)
        raise Exception("Failed to remove deck")


def delete_card(deck_id: int, card_id: int, permanent: int):
    """
    Delete a card by its ID.

    Args:
        card_id (int): The ID of the card to delete.
        permanent (int): If 1, perform a hard delete (permanently remove the card from the database).
                        If 0, perform a soft delete (update the modified time but keep the card).

    Returns:
        int: Number of rows deleted (0 if no card was deleted).
    """
    try:
        card = Card.get_or_none(Card.id == card_id, Deck.id == deck_id)
        if not card:
            raise Exception("Card not found")
        if permanent == 1:
            # Hard delete
            num_deleted = Card.delete().where(Card.id == card_id, Deck.id == deck_id).execute()
            return num_deleted
        else:
            card.modifiedtime = datetime.now()  # This just marks modification, not real trash delete
            card.save()
            return 1
    except Exception as e:
        print(e)
        raise Exception("Failed to remove card")


def get_card_due():
    """
    List out all the cards that are due
    """
    # TODO, return the list of cards that are due
    return []


def initiate_card_review():
    """
    Add the new cards for review
    """

    # TODO, get the card_ids excluding the ones that are not yet reviewed
    # load the new cards to for FSRS review
    query = Card.select(id)
    cards = [model_to_dict(card) for card in query]
    print(cards)


