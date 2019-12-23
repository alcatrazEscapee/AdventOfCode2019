# Day 20: Donut Maze

from utils import *
from collections import defaultdict
from typing import List, Dict


def main(lines: List[str]):
    grid = defaultdict(lambda: '?')
    letters = set()
    y_max, x_max = len(lines), max(len(lines[i]) for i in range(len(lines)))
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            tile = lines[y][x]
            if tile in ('.', '#'):
                grid[x, y] = tile
            elif tile.isalpha():
                letters.add((x, y))
    print_grid(grid, reverse_y=True)

    portals = defaultdict(list)
    for letter in letters:
        x, y = letter
        if (x + 1, y) in letters:
            portals[lines[y][x] + lines[y][x + 1]].append((x + 2, y) if grid[x + 2, y] == '.' else (x - 1, y))
        elif (x, y + 1) in letters:
            portals[lines[y][x] + lines[y + 1][x]].append((x, y + 2) if grid[x, y + 2] == '.' else (x, y - 1))

    start = portals['AA'][0]
    end = portals['ZZ'][0]
    portal_map = {}
    recursive_portal_map = {}
    for name, points in portals.items():
        if len(points) == 2:
            # normal portals for part 1
            portal_map[points[0]] = points[1]
            portal_map[points[1]] = points[0]

            # portals need to map to a point and +/- in level for part 2
            # -1 if points[0] is on the outside
            side = -1 if points[0][0] < 4 or points[0][1] < 4 or points[0][0] > x_max - 4 or points[0][1] > y_max - 4 else 1
            recursive_portal_map[points[0]] = (points[1][0], points[1][1], side)
            recursive_portal_map[points[1]] = (points[0][0], points[0][1], -side)

    print('Part 1:', bfs(grid, portal_map, start, end))
    print('Part 2:', bfs2(grid, recursive_portal_map, start, end))


def bfs(grid: Dict[Tuple[int, int], str], portals: Dict[Tuple[int, int], Tuple[int, int]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    paths = [(0, start)]
    visited = {start}
    while paths:
        path = paths.pop(0)
        if path[1] == end:
            return path[0]
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = path[1][0] + d[0], path[1][1] + d[1]
            if grid[new_pos] == '.' and new_pos not in visited:
                visited.add(new_pos)
                paths.append((path[0] + 1, new_pos))
        if path[1] in portals and portals[path[1]] not in visited:
            new_pos = portals[path[1]]
            visited.add(new_pos)
            paths.append((path[0] + 1, new_pos))


def bfs2(grid: Dict[Tuple[int, int], str], portals: Dict[Tuple[int, int], Tuple[int, int, int]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    actual_start = (*start, 0)
    actual_end = (*end, 0)
    paths = [(0, actual_start)]
    visited = {actual_start}
    while paths:
        path = paths.pop(0)
        pos = path[1][0:2]
        if path[1] == actual_end:
            return path[0]
        for d in ((0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)):
            new_pos = tuple(padd(path[1], d))
            if grid[new_pos[0], new_pos[1]] == '.' and new_pos not in visited:
                visited.add(new_pos)
                paths.append((path[0] + 1, new_pos))
        if pos in portals:
            portal = portals[pos]
            new_pos = portal[0], portal[1], portal[2] + path[1][2]
            if new_pos not in visited and new_pos[2] >= 0:
                visited.add(new_pos)
                paths.append((path[0] + 1, new_pos))


if __name__ == '__main__':
    main(get_input_lines())
