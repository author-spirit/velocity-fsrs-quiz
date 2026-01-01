"""
Spaced Repetition

Uses Py-FSRS service
Ref: https://github.com/open-spaced-repetition/py-fsrs
"""

from fsrs import Scheduler, Card, Rating
from playhouse.shortcuts import model_to_dict
from core.logs import logger
from models.cardreview import CardReview

class SpacedRepetition:

    def get_next_due(self, card_id: int, user_rating: Rating) -> dict:
        """
        Calculate the next due date for a card based on review rating.

        Args:
            card_info (dict): The card information as a dictionary, containing fields required by FSRS.
            rating (int or Rating, optional): The review rating (can be int or Rating enum). 
                If not provided, FSRS may determine due based on current data/state.

        Returns:
            dict: The card state after scheduling, including updated due date and FSRS state fields.
        """

        # TODO, test result with and without fuzzing
        scheduler = Scheduler(enable_fuzzing=False)
        cardreview = CardReview.get_or_none(CardReview.card == card_id)

        # for new card use card_id only
        if cardreview:
            # cardreview['difficulty'] = difficulty

            cardinfo = model_to_dict(cardreview, recurse=False)
            cardinfo["card_id"] = card_id
            del cardinfo["id"]
            logger.info("Previous Card Review")
            logger.info(cardinfo) 
            card = Card.from_dict(cardinfo)
        else:
            logger.info("Packing new card review")
            card = Card(card_id=card_id)

        logger.info(f"New User rating {user_rating}")
        
        reviewed_card, _ = scheduler.review_card(card, user_rating.value)
        logger.info("Next Due")
        logger.info(reviewed_card.to_json())

        self.save_cardreview(card_id, reviewed_card.to_dict())

        # To check retrievability
        # retrieve = scheduler.get_card_retrievability(reviewed_card)

        return reviewed_card.to_dict()

    def save_cardreview(self, card_id: int, result: dict) -> None:
        """
        Create a new CardReview if it doesn't exist, or update the existing one.
        Args:
            card_id (int): The card's ID.
            result (dict): State dictionary to update or create with.
        """
        cardreview = CardReview.get_or_none(CardReview.card == card_id)
        if cardreview:
            logger.info("Updating Card Review")
            logger.info(result)
            cardreview.state = result.get("state")
            cardreview.step = result.get("step")
            cardreview.stability = result.get("stability")
            cardreview.difficulty = result.get("difficulty")
            cardreview.due = result.get("due")
            cardreview.last_review = result.get("last_review")
            logger.info(model_to_dict(cardreview, recurse=False))
            cardreview.save()
        else:
            logger.info("Creating Card Review")
            logger.info(result)
            CardReview.create(
                card=card_id,
                state=result.get("state"),
                step=result.get("step", 1),
                stability=result.get("stability"),
                difficulty=result.get("difficulty"),
                due=result.get("due"),
                last_review=result.get("last_review"),
            )