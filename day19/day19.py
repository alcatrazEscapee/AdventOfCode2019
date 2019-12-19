# Day 19: Tractor Beam


from utils import *
from collections import defaultdict
from typing import Tuple


def main():
    grid = make_grid()
    print_grid(grid, reverse_y=True)
    bottom_left: Tuple[int, int] = max(grid.keys())  # somewhere on the bottom edge of the beam

    print('Part 1:', list(grid.values()).count('#'))

    while True:
        top_right = bottom_left[0] + 99, bottom_left[1] - 99
        if top_right[1] > 0:  # sanity check for positive y
            if in_range(top_right[0], top_right[1]):
                print('Part 2:', bottom_left[0] * 10_000 + (bottom_left[1] - 99))
                break

        # advance to the next candidate position
        bottom_left = bottom_left[0], bottom_left[1] + 1

        while not in_range(bottom_left[0], bottom_left[1]):
            bottom_left = bottom_left[0] + 1, bottom_left[1]


def make_grid() -> Dict[Tuple[int, int], str]:
    grid = defaultdict(lambda: '.')
    for x in range(50):
        for y in range(50):
            if in_range(x, y):
                grid[(x, y)] = '#'
    return grid


def in_range(px: int, py: int):
    return IntCode(CODE, [px, py]).run().outputs[0] == 1


CODE = get_input_intcode()

if __name__ == '__main__':
    main()
