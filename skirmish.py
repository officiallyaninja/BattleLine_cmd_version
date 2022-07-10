from __future__ import annotations

from typing import Tuple, Optional, List

from custom_errors import SquadNotFullError
from squad import Squad
from card import Card


class Skirmish:

    @classmethod
    def generate_random(cls) -> Skirmish:
        random_skirmish = Skirmish()
        random_skirmish.squads = (Squad.generate_random(), Squad.generate_random())
        return random_skirmish

    def __init__(self):
        self.squads: Tuple[Squad, Squad] = (Squad(), Squad())
        self.first: Optional[int] = None
        self.winner: Optional[int] = None

    def __get_winner_from_full_squads(self) -> Optional[int]:
        if self.winner is not None:
            return self.winner

        try:
            # if one of the squads is not full this will raise an exception
            formations_equal = self.squads[0].get_formation().value == self.squads[1].get_formation().value
        except SquadNotFullError:
            return None

        if formations_equal:
            if self[0].sum() == self[1].sum():
                return self.first
            else:
                return 0 if self[0].sum() > self[1].sum() else 1

        else:  # squads not equal
            return 0 if self[0].get_formation().value > self[1].get_formation().value else 1

    def get_winner(self, public_cards: List[Card]) -> Optional[int]:
        self.winner = self.__get_winner_from_full_squads()
        if self.winner is not None:
            return self.winner

        return None
        # TODO: implement this shit
        raise NotImplementedError()

    def add_card(self, card: Card, player: int) -> None:
        self[player].append(card)
        if self[player].is_full():
            self.first = player

    def __getitem__(self, item) -> Squad:
        if item in [0, 1]:
            return self.squads[item]
        else:
            raise IndexError(f"Skirmish only has 2 items, index entered was {item}")

    def __str__(self):
        rev = Squad()
        rev.cards = self[0][::-1]
        return f"{rev} | {self[1]}"
