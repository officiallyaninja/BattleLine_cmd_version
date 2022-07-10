from typing import List

from card import Card


class Hand:
    def __init__(self) -> None:
        self.cards: List[Card] = []

    def draw_card(self, deck: List[Card]):
        if len(deck) >= 0:
            self.cards.append(deck.pop())
        self.sort()

    def sort(self) -> None:
        self.cards = sorted(self.cards, key=lambda x: (x.color.value, x.value))

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def append(self, card: Card) -> None:
        self.cards.append(card)

    def __str__(self) -> str:
        result = ""
        for card_ in self.cards:
            result += str(card_) + " "
        return result[:-1]

    def __len__(self) -> int:
        return len(self.cards)


