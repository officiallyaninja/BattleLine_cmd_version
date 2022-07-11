from __future__ import annotations

from enum import Enum
from typing import List, Optional
import random

from custom_errors import CollectionFullError, SquadNotFullError
import card


class Formation(Enum):
    NIL = 0
    STRAIGHT = 1
    FLUSH = 2
    THREE_OF_A_KIND = 3
    STRAIGHT_FLUSH = 4


class Squad:

    @classmethod
    def generate_random(cls) -> Squad:
        x = Squad()
        for _ in range(random.randint(0, 3)):
            x.append(card.Card.generate_random())
        return x

    def __init__(self) -> None:
        self.cards: List[Optional[card.Card]] = [None, None, None]
        self.max_size = 3

    def append(self, card_: card.Card) -> None:
        for i in range(self.max_size):
            if self[i] is None:
                self.cards[i] = card_
                return
        raise CollectionFullError()

    def add_cards(self, cards: List[card]):
        for card_ in cards:
            self.append(card_)

    def is_full(self):
        return len(self) == self.max_size

    def sum(self):
        return sum(card_.value for card_ in self.cards)

    def get_formation(self) -> Formation:
        if not self.is_full():
            raise SquadNotFullError()

        cards = sorted(self.cards, key=lambda x: x.value)

        straight: bool = all(cards[i - 1].value == cards[i].value - 1 for i in range(1, self.max_size))
        flush: bool = all(card_.color == cards[0].color for card_ in cards)
        three_of_a_kind: bool = all(card_.value == cards[0].value for card_ in cards)

        if straight and flush:
            return Formation.STRAIGHT_FLUSH
        elif three_of_a_kind:
            return Formation.THREE_OF_A_KIND
        elif flush:
            return Formation.FLUSH
        elif straight:
            return Formation.STRAIGHT
        else:
            return Formation.NIL

    def copy(self) -> Squad:
        new_squad = Squad()
        new_squad.cards = self.cards.copy()
        new_squad.max_size = self.max_size
        return new_squad

    def __len__(self):
        return len(list(filter(lambda x: x is not None, self.cards)))

    def __str__(self) -> str:
        result = ""
        for card_ in self.cards:
            if card_ is None:
                card_ = " " * 2
            result += str(card_) + " "

        return result[:-1]

    def __getitem__(self, key):
        return self.cards[key]


