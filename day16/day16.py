# Day 16

"""
Reminders:
 - dicts, sets, sorting, Counter, enumerate, deque
 - padd, psub, pdot, pnorm1, pnorm2sq, protccw, protcw
 - gcd, lcm, min/max
 - IntCode, Cycle
"""

from utils import *


def part1(text):
    values = [int(c) for c in text]
    base_pattern = [0, 1, 0, -1]

    for phase in range(100):
        new_values = [0] * len(values)
        for pos in range(len(values)):
            pattern = []
            for p in range(len(base_pattern)):
                for i in range(1 + pos):
                    pattern.append(base_pattern[p])
            x = pattern.pop(0)
            pattern.append(x)
            for p in range(len(values)):
                new_values[pos] += values[p] * pattern[(p % len(pattern))]

        values = [(-v if v < 0 else v) % 10 for v in new_values]

    return ''.join(str(v) for v in values[0:8])


def part2(text: str):
    values = [int(c) for c in text][::-1]  # reverse the initial list
    total_length = len(values) * 10_000
    offset = int(text[0:7])
    offset = total_length - offset  # max index to calculate

    partial_sums = [0] * offset  # initialize partial sums
    for i in range(offset):
        partial_sums[i] = values[i % len(values)]

    for phase in range(100):  # calculate FFT
        new_partial_sums = [0] * offset
        new_partial_sums[0] = partial_sums[0]
        for pos in range(1, offset):
            new_partial_sums[pos] = new_partial_sums[pos - 1] + partial_sums[pos]

        partial_sums = [(-v if v < 0 else v) % 10 for v in new_partial_sums]

    return ''.join(str(v) for v in partial_sums[::-1][0:8])


if __name__ == '__main__':
    assert part1('80871224585914546619083218645595') == '24176176'
    assert part1('19617804207202209144916044189917') == '73745418'
    assert part1('69317163492948606335995924319873') == '52432133'

    print('Part 1:', part1(get_input()))

    assert part2('03036732577212944063491565474664') == '84462026'
    assert part2('02935109699940807407585447034323') == '78725270'
    assert part2('03081770884921959731165446850517') == '53553731'

    print('Part 2:', part2(get_input()))
