# Day 6: Universal Orbit Map
# Rank: 16 / 20

from utils import *


def main(elements):
    nodes = set()
    orbits = {}
    for edge in elements:
        left, right = edge.split(')')
        nodes.add(left)
        nodes.add(right)
        orbits[right] = left

    # Counts the number of orbits
    orbit_count = 0
    for node in nodes:
        while node in orbits:
            node = orbits[node]
            orbit_count += 1

    print('Part 1:', orbit_count)

    you = orbits["YOU"]
    san = orbits["SAN"]

    # Both paths from YOU and SAN to the root of the tree, then remove the common path elements
    you_to_start = []
    san_to_start = []
    while you in orbits:
        you_to_start.append(you)
        you = orbits[you]
    while san in orbits:
        san_to_start.append(san)
        san = orbits[san]

    # Eliminate common path elements
    while you_to_start[-1] == san_to_start[-1]:
        you_to_start.pop(-1)
        san_to_start.pop(-1)

    # The number of orbital transfers should be one less, but we remove the one connecting node above
    print('Part 2:', len(you_to_start) + len(san_to_start))


if __name__ == '__main__':
    main(get_input_lines())
