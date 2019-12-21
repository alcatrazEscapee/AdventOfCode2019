# Day 21: Springdroid Adventure
# Rank 168 / 100 (a whole 1 point!)

from utils import *


def main(droid_code: List[int], jump_code: str):
    runner = IntCode(droid_code)
    for c in jump_code:
        runner.inputs.append(ord(c))
    runner.run()
    return runner.outputs[-1]


if __name__ == '__main__':
    puzzle_input = get_input_intcode()
    # not A or (D and not C)
    print('Part 1:', main(puzzle_input, 'NOT C J\nAND D J\nNOT A T\nOR T J\nWALK\n'))
    # not A or ((E or H) and D and (not B or not C))
    print('Part 2:', main(puzzle_input, 'OR E J\nOR H J\nAND D J\nOR B T\nAND C T\nNOT T T\nAND T J\nNOT A T\nOR T J\nRUN\n'))
