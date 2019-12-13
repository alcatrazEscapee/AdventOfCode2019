# Day 2: 1202 Program Alarm
# Rank 13 / 17

from utils import *


def run(code: list, noun: int, verb: int) -> int:
    # Solution has been modified to use the IntCode class from later problems
    runner = IntCode(code, [])
    runner.code[1] = noun
    runner.code[2] = verb
    runner.run()
    return runner.code[0]


def find_result(code: list, target: int) -> int:
    for i in range(100):
        for j in range(100):
            if target == run(code, i, j):
                return i * 100 + j


if __name__ == '__main__':
    input_code = get_input_intcode()
    print('Part 1:', run(input_code, 12, 2))
    print('Part 2:', find_result(input_code, 19690720))
