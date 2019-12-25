# Day 17: Set and Forget

from utils import *
from collections import defaultdict


def check_cameras(values):
    runner = IntCode(values)
    runner.run()

    pos = (0, 0)
    grid = defaultdict(lambda: '?')

    while runner.outputs:
        p = runner.outputs.pop(0)
        if p == 10:
            pos = (0, pos[1] - 1)
        else:
            grid[pos] = chr(p)
            pos = (pos[0] + 1, pos[1])

    min_x, max_x = min_max([p[0] for p in grid.keys()])
    min_y, max_y = min_max([p[1] for p in grid.keys()])

    checksum = 0
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if grid[(i, j)] == grid[(i, j - 1)] == grid[(i, j + 1)] == grid[(i - 1, j)] == grid[(i + 1, j)] == '#':
                checksum += i * (max_y - j)

    print_grid(grid)
    print('Part 1', checksum)


def count_dust(values, path):
    runner = IntCode(values)
    runner.code[0] = 2
    for c in path:
        runner.inputs.append(ord(c))
    runner.run()
    print('Part 2:', runner.outputs[-1])


if __name__ == '__main__':
    puzzle_input = get_input_intcode()
    check_cameras(puzzle_input)

    # Part 2 was solved by hand (unfortunately, quite slowly) - see part2_notes.md
    count_dust(puzzle_input, 'A,A,B,B,C,B,C,B,C,A\nL,10,L,10,R,6\nR,12,L,12,L,12\nL,6,L,10,R,12,R,12\nn\n')
