from core.logs import logger
from models.card import Card
from models.deck import Deck
from models.cardreview import CardReview
from datetime import datetime
from typing import Union, Optional
import json
from playhouse.shortcuts import model_to_dict
from services.spacedrepetition import SpacedRepetition
from utils import helpers
from peewee import fn

PAGE_LIMIT = 10

class Flashcard:
    """Service class for managing flashcards, decks, and reviews."""

    @staticmethod
    def save_deck(data: dict) -> dict:
        """
        Saves a deck to the database. If 'id' is not present in data, creates a new deck.
        If 'id' is present, updates the existing deck with new information.

        Args:
            data (dict): Dictionary containing deck details such as 'id', 'name', and 'author'.

        Returns:
            dict: The saved deck as a dictionary.

        Raises:
            ValueError: If deck with id doesn't exist, or if deck name already exists.
        """
        deck_id = data.get("id")
        name = data.get("name")
        author = data.get("author")

        if not name:
            raise ValueError("Deck name is required.")

        # Check for duplicate name (excluding current deck if updating)
        existing_deck = Deck.get_or_none(Deck.name == name)
        if existing_deck and (not deck_id or existing_deck.id != deck_id):
            raise ValueError(f"Deck with name '{name}' already exists.")

        if not deck_id:
            # Create new deck
            deck = Deck(
                name=name,
                author=author,
                createdtime=datetime.now(),
                modifiedtime=datetime.now(),
            )
        else:
            # Update existing deck
            deck = Deck.get_or_none(Deck.id == deck_id)
            if not deck:
                raise ValueError(f"Deck with id '{deck_id}' does not exist.")
            
            # Update fields if provided
            if name and deck.name != name:
                deck.name = name
            if author and deck.author != author:
                deck.author = author
            deck.modifiedtime = datetime.now()

        deck.save()
        return model_to_dict(deck)

    @staticmethod
    def get_deck_by_id(id: int, filters: dict) -> dict:
        """Get the deck by id along with cards
        Args:
            id (int): Deck ID
            filters (dict): Filters for pagination
        Returns:
            dict: Deck Instance with cards
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
            deck_dict["cards"] = Flashcard.get_cards(id, filters)
            return deck_dict
        except Exception as e:
            logger.error(e)
            return {}

    @staticmethod
    def get_decks(filters: Optional[Union[dict, str]] = None) -> Union[dict, list]:
        """
        Get all decks
        Args:
            filters (Union[dict, str]): Filters for pagination and filtering
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
            query = query.where(~Deck.is_trash)

        query = query.limit(PAGE_LIMIT).offset(offset)
        return [model_to_dict(deck) for deck in query]

    @staticmethod
    def save_card(card_info: dict) -> dict:
        """
        Save a card information having question and answer
        Args:
            card_info (dict): A dictionary containing card details.
                For creation: should include 'deck_id', 'question', 'answer'.
                For update: should include 'id' (card id to update), and optional 'question', 'answer'.

        Returns:
            dict: The saved card as a dictionary.

        Raises:
            ValueError: If card with id doesn't exist or required fields are missing.
        """
        card_id = card_info.get("id")
        question = card_info.get("question")
        answer = card_info.get("answer")
        deck_id = card_info.get("deck_id")

        if not card_id:
            # Create new card
            if not deck_id:
                raise ValueError("Deck ID is required for creating a card.")
            if not question or not answer:
                raise ValueError("Question and answer are required for creating a card.")

            # Verify deck exists
            deck = Deck.get_or_none(Deck.id == deck_id)
            if not deck:
                raise ValueError(f"Deck with id '{deck_id}' does not exist.")

            card = Card(
                question=question,
                answer=answer,
                deck=deck_id,
                createdtime=datetime.now(),
                modifiedtime=datetime.now(),
            )
        else:
            # Update existing card
            card = Card.get_or_none(Card.id == card_id)
            if not card:
                raise ValueError(f"Card with id '{card_id}' does not exist.")
            
            # Update fields if provided
            if question is not None and card.question != question:
                card.question = question
            if answer is not None and card.answer != answer:
                card.answer = answer
            card.modifiedtime = datetime.now()

        # Peewee's save() handles both insert and update
        card.save()
        return model_to_dict(card, recurse=False)

    @staticmethod
    def get_cards(deck_id: int, filters: Union[dict, str]) -> list:
        """Get Cards belongs to deck
        Args:
            deck_id (int): Deck ID
            filters (Union[dict, str]): Filters for pagination
        Return:
            List of Cards
        """
        if isinstance(filters, str):
            try:
                filters = json.loads(filters)
            except Exception:
                filters = {}

        if not filters or not isinstance(filters, dict):
            filters = {"page": 1}

        query = Card.select()
        page = int(filters.get("page", 1))
        offset = (page - 1) * PAGE_LIMIT
        query = query.where(Card.deck == deck_id, ~Card.is_trash).limit(PAGE_LIMIT).offset(offset)
        return [model_to_dict(card, recurse=False) for card in query]

    @staticmethod
    def is_deck_in_use(deck_id: int) -> bool:
        """
        Check whether given deck has any cards (non-trashed).
        Args:
            deck_id (int): Deck to check
        Returns:
            True if deck has cards, False otherwise
        """
        card_count = Card.select().where(Card.deck == deck_id, ~Card.is_trash).count()
        return card_count > 0

    @staticmethod
    def delete_deck(deck_id: int) -> bool:
        """
        Delete a deck by its ID. Only deletes if deck has no cards.

        Args:
            deck_id (int): The ID of the deck to delete.
        Returns:
            bool: True if the deck was deleted.

        Raises:
            ValueError: If the deck with the given ID does not exist or has cards.
            RuntimeError: If an error occurs during deletion.
        """
        try:
            deck = Deck.get_or_none(Deck.id == deck_id)
            if not deck:
                raise ValueError(f"Deck Id '{deck_id}' does not exist.")

            # Check if deck has cards
            if Flashcard.is_deck_in_use(deck_id):
                raise ValueError(f"Cannot delete deck '{deck_id}' because it contains cards. Please delete or move cards first.")

            num_deleted = Deck.delete().where(Deck.id == deck_id).execute()
            if num_deleted == 0:
                raise ValueError(f"Deck Id '{deck_id}' does not exist.")
            return True
        except ValueError:
            raise
        except Exception as e:
            logger.error(e)
            raise RuntimeError("Failed to delete deck") from e

    @staticmethod
    def trash_deck(deck_id: int) -> bool:
        """
        Mark the deck as trashed (set is_trash to True).
        Only trashes if deck has no cards.

        Args:
            deck_id (int): The ID of the deck to trash.
        Returns:
            bool: True if successful.

        Raises:
            ValueError: If the deck with the given ID does not exist or has cards.
            RuntimeError: If an error occurs during trash.
        """
        try:
            deck = Deck.get_or_none(Deck.id == deck_id)
            if not deck:
                raise ValueError(f"Deck Id '{deck_id}' does not exist.")

            # Check if deck has cards
            if Flashcard.is_deck_in_use(deck_id):
                raise ValueError(f"Cannot trash deck '{deck_id}' because it contains cards. Please delete or move cards first.")

            deck.is_trash = True
            deck.modifiedtime = datetime.now()
            deck.save()
            return True
        except ValueError:
            raise
        except Exception as e:
            logger.error(e)
            raise RuntimeError("Failed to trash deck") from e

    @staticmethod
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

    @staticmethod
    def trash_card(card_id: int) -> bool:
        """
        Mark the card as trashed (set is_trash to True) by card_id in a deck.
        Args:
            card_id (int): The ID of the card to trash.
        Returns:
            bool: True if successful, raises Exception otherwise.
        Raises:
            ValueError: If the card with the given ID does not exist.
            RuntimeError: If an error occurs during trash.
        """
        try:
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

    @staticmethod
    def get_due_cards(filters: Optional[Union[dict, str]] = None):
        """
        List out all the cards that are due
        Args:
            filters (Optional[Union[dict, str]]): Filters for pagination and deck filtering
        Returns:
            list: List of due cards
        """
        if filters is None:
            filters = {}
        elif isinstance(filters, str):
            filters = helpers.safe_json_parse(filters)
            filters = filters or {}

        page = int(filters.get("page", 1))
        offset: int = (page - 1) * PAGE_LIMIT

        query = CardReview.select()

        if "deck_id" in filters:
            deck_id = filters.get("deck_id")
            query = query.join(Card).where(Card.deck == deck_id, ~Card.is_trash)

        due_cards = query.where(CardReview.due <= datetime.now()).limit(PAGE_LIMIT).offset(offset)
        return [model_to_dict(card, recurse=False) for card in due_cards]

    @staticmethod
    def get_due_decks(filters: dict) -> list:
        page = int(filters.get("page", 1))
        offset: int = (page - 1) * PAGE_LIMIT

        query = (
            CardReview
            .select(
                fn.COUNT(CardReview.id).alias("count"),
                Deck.id.alias("deck_id"),
                Deck.name.alias("deck_name")
            )
            .join(Card, on=(Card.id == CardReview.card_id))
            .join(Deck, on=(Deck.id == Card.deck))
            .group_by(Deck.id)
            .limit(PAGE_LIMIT)
            .offset(offset)
        )

        results = []
        for row in query.dicts():
            results.append({
                "count": row["count"],
                "deck_id": row["deck_id"],
                "deck_name": row["deck_name"]
            })
        return results

    @staticmethod
    def get_next_due(card_id: int, user_rating: int):
        """
        Get the due of given card
        Args:
            card_id (int): Card Id
            user_rating (int): card difficulty
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
