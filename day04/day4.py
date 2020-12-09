# Day 4: Secure Container

from typing import Tuple
from collections import Counter


def count_valid_passwords(min_value: int, max_value: int):
    part1 = part2 = 0

    for num in range(min_value, max_value + 1):
        password = str(num)
        if ''.join(sorted(password)) == password:
            digit_counts = Counter(password)
            if max(digit_counts.values()) >= 2:
                part1 += 1
                if 2 in digit_counts.values():
                    part2 += 1

    print('Part 1:', part1)
    print('Part 2:', part2)


if __name__ == '__main__':
    count_valid_passwords(156218, 652527)
