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


# Main function


def main():
    global current_player_index
    while get_winner() is None:  # this line causes calculation of "provable wins"
        current_player_index = (current_player_index + 1) % 2
        print_battles()
        print_current_hand()

        selected_card, selected_index = get_inputs()
        play_card(selected_card, selected_index)


# Helper functions


def print_battles():
    for i, skirmish in enumerate(battles):
        print(f"[{i + 1}] {skirmish}")


def print_current_hand():
    print(players[current_player_index])


def get_inputs() -> Tuple[Card, int]:
    selected_card = get_input_card()
    # TODO: add undo
    print(f"you have selected {selected_card}")
    selected_index = get_input_battle_index()
    return selected_card, selected_index


def get_input_card() -> Card:
    hand: Hand = players[current_player_index]
    card_index = input_handler.get_int_in_range(1, len(hand) + 1, "enter index of card you want to play: ") - 1

    return hand.pop(card_index)


def get_input_battle_index() -> int:
    valid_inputs = []
    for i, skirmish in enumerate(battles):
        if skirmish.winner is None:
            valid_inputs.append(i + 1)

    index = input_handler.get_int_in_list(valid_inputs, "enter skirmish you would like to play card to") - 1
    return index


def play_card(card: Card, battle_index: int) -> None:
    battles[battle_index].add_card(card, current_player_index)
    players[current_player_index].draw_card(deck)


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
