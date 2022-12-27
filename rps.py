import random

RPS_DICT = {
    'R': 'Rock',
    'P': 'Paper',
    'S': 'Scissor'
}

WINNER_DICT = {
    'R': 'S',
    'P': 'R',
    'S': 'P'
}


def get_bot_choice() -> str:
    return random.choice(tuple(RPS_DICT.keys()))


def get_winner(p1_choice: str, p2_choice: str) -> str:
    if p1_choice == p2_choice:
        return 'draw'
    elif p1_choice == WINNER_DICT[p2_choice]:
        return 'p2'
    elif p2_choice == WINNER_DICT[p1_choice]:
        return 'p1'
