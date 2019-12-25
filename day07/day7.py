# Day 7: Amplification Circuit
# Rank 36 / 25

from itertools import permutations
from utils import *


def part1(code: list):
    values = set()
    for settings in permutations(range(5)):
        out = [0]
        for i in range(5):
            out = IntCode(code, [settings[i], *out]).run().outputs
        values.add(out[0])
    print('Part 1:', max(values))


def part2(code: list):
    values = set()
    for settings in permutations(range(5, 10)):
        amplifiers = [IntCode(code, [settings[i]]) for i in range(5)]

        # Initial starting input
        amplifiers[0].inputs.append(0)

        # Link outputs to inputs
        for i in range(5):
            amplifiers[i].outputs = amplifiers[(i + 1) % 5].inputs

        # Run until all are finished
        while any(a.running for a in amplifiers):
            for a in amplifiers:
                a.run()

        values.add(amplifiers[4].outputs[0])

    print('Part 2:', max(values))


if __name__ == '__main__':
    input_code = get_input_intcode()
    part1(input_code)
    part2(input_code)
