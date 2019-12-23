# Day 22: Slam Shuffle

from utils import *
from typing import Tuple, Callable


def shuffle(rules: List[Tuple[int, int]], length: int) -> List[int]:
    deck = [*range(length)]
    for rule in rules:
        deck = SHUFFLE[rule[0]](deck, rule[1])
    return deck


def shuffle_fast(rules: List[Tuple[int, int]], length: int) -> Tuple[int, int]:
    a, b = 0, 1
    for rule in rules:
        a, b = SHUFFLE_FAST[rule[0]](a, b, rule[1], length)
    return a, b


def get_rule(r: str) -> Tuple[int, int]:
    values = ints(r)
    if 'cut' in r:
        return CUT, values[0]
    elif 'new stack' in r:
        return REVERSE, 0
    elif 'increment' in r:
        return DEAL, values[0]


def deal_increment(deck: List[int], inc: int) -> List[int]:
    size = len(deck)
    new_deck = [0] * size
    for i in range(size):
        new_deck[(i * inc) % size] = deck[i]
    return new_deck


REVERSE = 0
CUT = 1
DEAL = 2

# Top = low, bottom = high
SHUFFLE: List[Callable[[List[int], int], List[int]]] = [
    lambda deck, unused: deck[::-1],
    lambda deck, num: deck[num:] + deck[:num],
    deal_increment
]

# deck = a + b * n
SHUFFLE_FAST: List[Callable[[int, int], Tuple[int, int]]] = [
    lambda a, b, unused, m: ((a - b) % m, -b % m),  # reverse by negating b, and subtracting b from a to get the last element
    lambda a, b, n, m: ((a + b * n) % m, b),  # cut = change the offset
    lambda a, b, n, m: (a, (b * pow(n, -1, m)) % m)  # deal with increment uses modular inverse
]

if __name__ == '__main__':
    puzzle_rules = [get_rule(r) for r in get_input_lines()]
    print('Part 1:', shuffle(puzzle_rules, 10007).index(2019))

    deck_length = 119315717514047
    repeats = 101741582076661
    offset, increment = shuffle_fast(puzzle_rules, deck_length)
    # Apply the repitions via geometric series
    offset *= (1 - pow(increment, repeats, deck_length)) * pow(1 - increment, -1, deck_length)
    increment = pow(increment, repeats, deck_length)

    print('Part 2:', (offset + increment * 2020) % deck_length)
