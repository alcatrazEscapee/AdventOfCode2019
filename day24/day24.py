# Day 24: Planet of Discord
# Rank 59 / 11

from utils import *
from typing import Tuple, DefaultDict, Union

Point2 = Tuple[int, int]
Point3 = Tuple[int, int, int]


def find_repeated_state(grid: DefaultDict[Point2, int]) -> int:
    state = frozenset(grid.keys())
    prev = set()
    while state not in prev:
        prev.add(state)
        new_grid = defaultdict(int)
        for x in range(5):
            for y in range(5):
                s = sum((grid[x, y - 1], grid[x, y + 1], grid[x + 1, y], grid[x - 1, y]))
                if cell_rule(grid[x, y], s):
                    new_grid[x, y] = 1
        grid = new_grid
        state = frozenset(grid.keys())
    return sum(1 << (p[0] + p[1] * 5) for p in state)


def simulate_recursive(grid: DefaultDict[Point3, int]) -> int:
    for _ in range(200):
        new_grid = defaultdict(int)
        min_level, max_level = min_max(set(p[2] for p in grid.keys()))
        for x in range(5):
            for y in range(5):
                # skip the center, there's a recursive grid there
                if (x, y) != (2, 2):
                    for level in range(min_level - 1, max_level + 2):
                        s = adj_points_recursive(grid, x, y, level)
                        if cell_rule(grid[x, y, level], s):
                            new_grid[x, y, level] = 1
        grid = new_grid
    return len(grid.keys())


def adj_points_recursive(grid: DefaultDict[Point3, int], x: int, y: int, level: int) -> int:
    # This gets the adjacent point that have bugs, considering the recursive nature of the grid
    # It checks four possible cases: adjacent tiles to the center, or edge tiles, and adds the respective other adjacent tiles
    s = sum((grid[x, y - 1, level], grid[x, y + 1, level], grid[x + 1, y, level], grid[x - 1, y, level]))
    if (x, y) == (2, 1):
        for xi in range(5):
            s += grid[xi, 0, level + 1]
    elif (x, y) == (2, 3):
        for xi in range(5):
            s += grid[xi, 4, level + 1]
    elif (x, y) == (1, 2):
        for yi in range(5):
            s += grid[(0, yi, level + 1)]
    elif (x, y) == (3, 2):
        for yi in range(5):
            s += grid[(4, yi, level + 1)]
    else:
        if x == 0:
            s += grid[(1, 2, level - 1)]
        elif x == 4:
            s += grid[(3, 2, level - 1)]
        if y == 0:
            s += grid[(2, 1, level - 1)]
        elif y == 4:
            s += grid[(2, 3, level - 1)]
    return s


def build_grid(lines: List[str], is3d: bool) -> DefaultDict[Union[Point2, Point3], int]:
    grid = defaultdict(int)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                if is3d:
                    grid[(x, y, 0)] = 1
                else:
                    grid[(x, y)] = 1
    return grid


def cell_rule(value: int, sum_adj: int) -> int:
    # This is the cell rule used by the cellular automata
    return sum_adj == 1 if value == 1 else sum_adj in (1, 2)


if __name__ == '__main__':
    puzzle_input = get_input_lines()
    print('Part 1:', find_repeated_state(build_grid(puzzle_input, False)))
    print('Part 2:', simulate_recursive(build_grid(puzzle_input, True)))
