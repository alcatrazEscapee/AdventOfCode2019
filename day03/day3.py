# Day 3: Crossed Wires
# Rank 42 / 53

from utils import *


def main():
    text = get_input_lines()
    wire1, wire2 = walk_wire(text[0]), walk_wire(text[1])
    intersections = wire1.keys() & wire2.keys()

    print('Part 1:', min(abs(p[0]) + abs(p[1]) for p in intersections))
    print('Part 2:', min(wire1[p] + wire2[p] for p in intersections))


def walk_wire(line):
    pos = (0, 0)
    points = {}
    count = 0
    for d in line.split(','):
        direction = d[0]
        length = int(d[1:])
        for _ in range(length):
            step = DIRECTIONS[direction]
            pos = pos[0] + step[0], pos[1] + step[1]
            count += 1
            if pos not in points:
                points[pos] = count
    return points


DIRECTIONS = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}

if __name__ == '__main__':
    main()
