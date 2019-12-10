# Day 10

from utils import *
from typing import Set
from math import atan2, pi


def build_asteroids(text: str) -> Set[tuple]:
    asteroids = set()
    for i, line in enumerate(text.split('\n')):
        for j, c in enumerate(line):
            if c == '#':
                asteroids.add((j, i))
    return asteroids


def best_location(asteroids: Set[tuple]):
    sights = {}
    for point in asteroids:
        blocked = set()
        for other in asteroids:
            if point != other:
                # find all integer points between the two points
                rays = ray_int(point, other)
                if any(p in asteroids for p in rays):
                    blocked.add(other)
        sights[point] = len(asteroids) - len(blocked) - 1
    return max(sights.items(), key=lambda x: x[1])


def destroy_them_with_lazors(asteroids: Set[tuple], start: tuple):
    asteroid_data = set()  # asteroid (x, y), angle, norm2sq
    for asteroid in asteroids - {start}:
        delta = psub(asteroid, start)
        angle = atan2(delta[0], delta[1]) + pi
        norm = pnorm2sq(delta)
        asteroid_data.add((asteroid, angle, norm))

    current_angle = 2 * pi
    target_num = 1
    target = None
    while asteroid_data and target_num <= 200:
        # Find the smallest angle delta (not equal to zero unless the first shot), then the closest
        target = min(asteroid_data, key=lambda x: (current_angle == x[1] or target_num == 1, (current_angle - x[1]) % (2 * pi), x[2]))
        asteroid_data.remove(target)
        current_angle = target[1]
        target_num += 1
    return target


if __name__ == '__main__':

    assert best_location(build_asteroids('.#..#\n.....\n#####\n....#\n...##')) == ((3, 4), 8)
    assert best_location(build_asteroids('......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####')) == ((5, 8), 33)
    assert best_location(build_asteroids('#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.')) == ((1, 2), 35)
    assert best_location(build_asteroids('.#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..')) == ((6, 3), 41)

    asteroid_map = build_asteroids(get_input())
    station, visible_count = best_location(asteroid_map)
    target, target_angle, target_dist = destroy_them_with_lazors(asteroid_map, station)

    print('Part 1:', visible_count)
    print('Part 2:', target[0] * 100 + target[1])
