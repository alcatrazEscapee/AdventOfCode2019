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
    step = 0
    for d in line.split(','):
        direction = d[0]
        length = int(d[1:])
        for _ in range(length):
            if direction == 'U':
                pos = pos[0], pos[1] + 1
            elif direction == 'L':
                pos = pos[0] - 1, pos[1]
            elif direction == 'R':
                pos = pos[0] + 1, pos[1]
            elif direction == 'D':
                pos = pos[0], pos[1] - 1
            step += 1
            if pos not in points:
                points[pos] = step
    return points


if __name__ == '__main__':
    main()
