# Day 18: Many-Worlds Interpretation

from utils import *
from collections import defaultdict
from heapq import heappop, heappush
from typing import Dict, Tuple, List, Set, FrozenSet


def find_shortest_path(input_lines: List[str]) -> int:
    grid, keys, starts = build_grid(input_lines)  # build the grid from the puzzle input
    # print_grid(grid)
    key_map = build_key_map(grid, starts, keys)  # (BFS) build a map of key -> key and distance / required keys to traverse as a graph
    # print_key_map(key_map)
    return search_key_map(key_map, keys, len(starts))  # (Dijkstra's) traverse the graph from key to key to find the shortest path


def build_grid(lines: List[str]) -> Tuple[Dict[Tuple[int, int], str], Dict[str, Tuple[int, int]], List[Tuple[int, int]]]:
    grid = defaultdict(lambda: '?')
    keys = {}
    starts = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            tile = lines[y][x]
            if tile == '@':
                starts.append((x, -y))
                grid[(x, -y)] = '.'
            else:
                if tile.islower():
                    keys[tile] = x, -y
                grid[(x, -y)] = tile
    return grid, keys, starts


def build_key_map(grid: Dict[Tuple[int, int], str], starts: List[Tuple[int, int]], keys: Dict[str, Tuple[int, int]]) -> Dict[str, Dict[str, Tuple[int, Set[str]]]]:
    key_map = {}
    for i, start in enumerate(starts):
        key_map[str(i)] = build_key_path(grid, start)
    for key, key_pos in keys.items():
        key_map[key] = build_key_path(grid, key_pos)
    return key_map


def build_key_path(grid: Dict[Tuple[int, int], str], start: Tuple[int, int]) -> Dict[str, Tuple[int, Set[str]]]:
    key_path: Dict[str, Tuple[int, Set[str]]] = {}
    visited: Set[Tuple[int, int]] = {start}
    paths: List[Tuple[Tuple[int, int], int, Set[str]]] = [(start, 0, set())]
    while paths:
        path = heappop(paths)
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = path[0][0] + d[0], path[0][1] + d[1]
            tile = grid[new_pos]
            if tile != '#' and new_pos not in visited:
                new_keys = path[2]
                if tile.isupper():
                    # door, so mark it requires a key
                    new_keys = path[2] | {tile.lower()}
                elif tile.islower():
                    # key so mark an endpoint
                    key_path[tile] = path[1] + 1, path[2]
                visited.add(new_pos)
                paths.append((new_pos, path[1] + 1, new_keys))
    return key_path


def search_key_map(key_map: Dict[str, Dict[str, Tuple[int, Set[str]]]], all_keys: Dict[str, Tuple[int, int]], num_starts: int) -> int:
    starts = tuple(str(i) for i in range(num_starts))
    paths: List[Tuple[int, Tuple[str], FrozenSet[str]]] = [(0, starts, frozenset())]  # distance, pos (by key), keys
    visited: Dict[Tuple[Tuple[str], FrozenSet[str]], int] = defaultdict(int)
    while paths:
        path = heappop(paths)  # use heap here because not all steps are the same distance
        if len(path[2]) == len(all_keys.keys()):
            return path[0]
        for curr_idx, curr_key in enumerate(path[1]):  # for each robot we want to move
            for next_key, next_path in key_map[curr_key].items():  # for each next key we want to move to
                if next_key not in path[2]:  # if we haven't already collected this key
                    next_keys = frozenset(path[2] | {next_key})
                    next_pos = path[1][:curr_idx] + (next_key,) + path[1][curr_idx + 1:]  # replaces the single key/pos in the tuple
                    node_id = (next_pos, next_keys)
                    dist = path[0] + next_path[0]
                    if (node_id not in visited.keys() or visited[node_id] > dist) and len(next_path[1] - path[2]) == 0:  # if we can travel this path (having the required keys), and it's a shorter path than previously found
                        heappush(paths, (dist, next_pos, next_keys))
                        visited[node_id] = dist


def print_key_map(key_map: Dict[str, Dict[str, Tuple[int, Set[str]]]]):
    # used for debugging, shows the key -> key connections
    for key, val in key_map.items():
        print(key, ':')
        for key2, val2 in val.items():
            print('\t', key2, ':', val2)


if __name__ == '__main__':
    print('Part 1:', find_shortest_path(get_input_lines('./input_part1.txt')))
    print('Part 2:', find_shortest_path(get_input_lines('./input_part2.txt')))
