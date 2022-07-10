from __future__ import annotations

from enum import Enum
from typing import List
import random

from termcolor import colored


class Color(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"


class Card:
    @classmethod
    def get_deck(cls) -> List[Card]:
        deck: List[Card] = []
        for color in Color:
            for num in range(1, 11):
                deck.append(Card(num, color))
        return deck

    @classmethod
    def generate_random(cls) -> Card:
        return Card(random.randint(1, 10), random.choice(list(Color)))

    def __init__(self, value: int, color: Color) -> None:
        self.value: int = value
        self.color: Color = color

    def __str__(self) -> str:
        result = colored(str(self.value), self.color.value)
        if self.value < 10:
            result += " "
        return result
