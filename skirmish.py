from __future__ import annotations

import itertools
from typing import Tuple, Optional, List

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

        # if one of the squads is not full this will raise an exception
        formations_equal = self.squads[0].get_formation().value == self.squads[1].get_formation().value

        if formations_equal:
            if self[0].sum() == self[1].sum():
                return self.first
            else:
                return 0 if self[0].sum() > self[1].sum() else 1

        else:  # squads not equal
            return 0 if self[0].get_formation().value > self[1].get_formation().value else 1

    def get_winner(self, public_cards: List[Card]) -> Optional[int]:
        if self.winner is not None:
            return self.winner
        if all(squad_.is_full() for squad_ in self.squads):
            self.winner = self.__get_winner_from_full_squads()
            return self.winner

        possible_cards: List[Card] = [card for card in Card.get_deck() if card not in public_cards]
        available_slots = tuple(squad_.max_size - len(squad_) for squad_ in self.squads)

        prospective_winner = None
        for cards_for_skirmish in itertools.combinations(possible_cards, sum(available_slots)):
            for cards_for_squad_0 in itertools.combinations(cards_for_skirmish, available_slots[0]):
                cards_for_squad_1 = [card for card in cards_for_skirmish if card not in cards_for_squad_0]
                copy = self.copy()
                copy.add_cards(cards_for_squad_0, 0)
                copy.add_cards(cards_for_squad_1, 1)

                winner = copy.__get_winner_from_full_squads()

                if prospective_winner is None:
                    prospective_winner = winner
                if prospective_winner != winner:
                    return None

        self.winner = prospective_winner
        return self.winner

    def copy(self) -> Skirmish:
        new_skirmish = Skirmish()
        new_skirmish.squads = (self[0].copy(), self[1].copy())
        new_skirmish.first = self.first
        return new_skirmish

    def add_card(self, card: Card, player: int) -> None:
        self[player].append(card)
        if self[player].is_full() and self.first is None:
            self.first = player

    def add_cards(self, cards: List[Card], player: int):
        for card in cards:
            self.add_card(card, player)

    def __getitem__(self, item) -> Squad:
        if item in [0, 1]:
            return self.squads[item]
        else:
            raise IndexError(f"Skirmish only has 2 items, index entered was {item}")

    def __str__(self):
        rev = Squad()
        rev.cards = self[0][::-1]
        return f"{rev} | {self[1]}"
