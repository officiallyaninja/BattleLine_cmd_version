from typing import Tuple, List, Optional
import random

import input_handler
from skirmish import Skirmish
from card import Card
from hand import Hand

# initial setup

deck: List[Card] = Card.get_deck()
random.shuffle(deck)

players: Tuple[Hand, Hand] = (Hand(), Hand())
for player in players:
    while len(player) < 7:
        player.draw_card(deck)

battles: List[Skirmish] = [Skirmish() for _ in range(9)]

current_player_index: int = 1


# Actual game loop

def main():
    global current_player_index
    while get_winner() is None:  # this line causes calculation of "provable wins"
        current_player_index = (current_player_index + 1) % 2
        print_battles()
        print_current_hand()
        selected_card = get_input_card()
        print(selected_card)


def print_battles():
    for i, skirmish in enumerate(battles):
        print(f"[{i}] {skirmish}")


def print_current_hand():
    global current_player_index
    print(players[current_player_index])


def get_input_card() -> Card:
    global current_player_index
    hand: Hand = players[current_player_index]
    card_index = input_handler.get_int_in_range(1, len(hand) + 1)

    return hand.pop(card_index)

def get_input_battle_index() -> int:
    

def get_winner() -> Optional[int]:
    global battles

    winners: List[int] = list(map(lambda x: x.get_winner(get_public_cards(battles)), battles))
    for player_index in [0, 1]:
        if winners.count(player_index) >= 5:
            return player_index
        for i in range(2, len(battles)):
            if battles[i] == battles[i - 1] == battles[i - 2] == player_index:
                return player_index


def get_public_cards(battle_list: List[Skirmish]) -> List[Card]:
    public_cards = []
    for skirmish in battles:
        for squad in skirmish:
            for card in squad:
                public_cards.append(card)
    return public_cards


if __name__ == '__main__':
    main()