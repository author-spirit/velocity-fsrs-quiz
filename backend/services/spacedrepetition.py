"""
Spaced Repetition

Uses Py-FSRS service
Ref: https://github.com/open-spaced-repetition/py-fsrs
"""

from fsrs import Scheduler, Card, Rating

RATINGS = {
    1: Rating.Again,
    2: Rating.Hard,
    3: Rating.Good,
    4: Rating.Easy
}

class SpacedRepetition:

    def get_next_due(self, card_info: dict, rating: int = None) -> dict:
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


        # for new card use card_id only
        if 'state' in card_info:
            card = Card.from_dict(card_info)
        else:
            card = Card(card_id=card_info.get("card_id"))

        rating = RATINGS.get(rating, RATINGS[3])        # REVIEW, Default Good
        
        scheduled_card, _ = scheduler.review_card(card, rating)
        print("Due Date", scheduled_card.to_json())

        # To check retrievability
        retrieve = scheduler.get_card_retrievability(scheduled_card)
        print(retrieve)

        return scheduled_card.to_dict()