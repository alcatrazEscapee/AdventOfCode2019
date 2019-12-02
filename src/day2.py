# Day 2: 1202 Program Alarm
# Rank 13 / 17

from src.utils import *


def run(noun: int, verb: int) -> int:
    values = [*ints(get_input(2))]
    values[1] = noun
    values[2] = verb
    pointer = 0
    while values[pointer] != 99:
        if values[pointer] == 1:
            values[values[pointer + 3]] = values[values[pointer + 1]] + values[values[pointer + 2]]
        elif values[pointer] == 2:
            values[values[pointer + 3]] = values[values[pointer + 1]] * values[values[pointer + 2]]
        pointer += 4
    return values[0]


def find_result(target: int) -> int:
    for i in range(100):
        for j in range(100):
            if target == run(i, j):
                return i * 100 + j


if __name__ == '__main__':
    print('Part 1', run(12, 2))
    print('Part 2', find_result(19690720))
