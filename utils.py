# AoC Utils

import re
import math
import functools

from collections import defaultdict
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Tuple, TypeVar


def get_input(path: str = './input.txt') -> str:
    with open(path) as f:
        return f.read()


def get_input_lines(path: str = './input.txt') -> List[str]:
    return get_input(path).split('\n')


def ints(text: str) -> Tuple[int, ...]:
    return tuple(map(int, re.findall('([\-+]?\d+)', text)))


def floats(text: str) -> Tuple[float, ...]:
    return tuple(map(float, re.findall('([\-+]?\d*(?:\d|\d\.|\.\d)\d*)', text)))


Number = TypeVar('Number', int, float)


# Geometry
def padd(x: Iterable[Number], y: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(a + b for a, b in zip(x, y))


def psub(x: Iterable[Number], y: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(a - b for a, b in zip(x, y))


def pmul(x: Iterable[Number], a: Number) -> Tuple[Number, ...]:
    return tuple(a * y for y in x)


def pdot(x: Iterable[Number], y: Iterable[Number]) -> Number:
    return sum(a * b for a, b in zip(x, y))


def pnorm1(x: Iterable[Number], y: Iterable[Number] = None) -> Number:
    if y is not None:
        x = psub(x, y)
    return sum(map(abs, x))


def pnorm2sq(x: Iterable[Number], y: Iterable[Number] = None) -> Number:
    if y is not None:
        x = psub(x, y)
    return sum(i * i for i in x)


def protccw(x: Tuple[Number, Number]) -> Tuple[Number, Number]:
    return -x[1], x[0]


def protcw(x: Tuple[Number, Number]) -> Tuple[Number, Number]:
    return x[1], -x[0]


def psign(x: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(sign(y) for y in x)


def pabs(x: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(abs(y) for y in x)


def min_max(x: Iterable[Number]) -> Tuple[Number, Number]:
    return min(x), max(x)


def sign(a: Number) -> Number:
    return 0 if a == 0 else (-1 if a < 0 else 1)


def lcm(a: int, b: int) -> int:
    """ Return lowest common multiple. """
    return a * b // math.gcd(a, b)


def gcd_iter(sequence: Iterable[int]) -> int:
    """ Return greatest common divisor of a list """
    return functools.reduce(math.gcd, sequence)


def lcm_iter(sequence: Iterable[int]) -> int:
    return functools.reduce(lcm, sequence)


def mod_inv(x: Number, m: Number) -> int:
    return pow(x, -1, m)


def ray_int(start: Iterable[int], end: Iterable[int]) -> list:
    """ Returns a list of tuples of the points in a ray cast from start to end, not including either """
    deltas = psub(end, start)
    delta_gcd = gcd_iter(deltas)
    points = []
    if delta_gcd > 1:
        for d in range(1, delta_gcd):
            p = padd(start, pmul(deltas, d / delta_gcd))
            if all(int(x) == x for x in p):
                points.append(tuple(int(x) for x in p))
    return points


def make_grid(grid_text: str) -> Dict[Tuple[int, int], Optional[str]]:
    """ Constructs a dictionary based grid from an ASCII / character representation
    :param grid_text:
    :return:
    """
    grid = defaultdict(lambda: None)
    for y, line in enumerate(grid_text.split('\n')):
        for x, c in enumerate(line):
            grid[x, y] = c
    return grid


def print_grid(grid_objects: Dict[Tuple[int, int], Any], values_map: Optional[Dict[Any, str]] = None, padding: int = 0, reverse_y: bool = True, reverse_x: bool = False):
    """ Prints a grid, represented as a map from points to values, to the console.
    Default reverse_x = False, reverse_y = True uses quadrant IV sign convention (Right = +x, Down = +y)
    With reverse_y = True, uses quadrant I sign convention (Right = +x, Up = +y)
    """
    def pixel(p: Any) -> str:
        if values_map is None:
            return str(p)
        else:
            return values_map[p] if p in values_map else '?'

    min_x = min(p[0] for p in grid_objects.keys()) - padding
    max_x = max(p[0] for p in grid_objects.keys()) + padding
    min_y = min(p[1] for p in grid_objects.keys()) - padding
    max_y = max(p[1] for p in grid_objects.keys()) + padding
    range_x = range(max_x, min_x - 1, -1) if reverse_x else range(min_x, max_x + 1)
    range_y = range(min_y, max_y + 1) if reverse_y else range(max_y, min_y - 1, -1)

    print('\n'.join(''.join(pixel(grid_objects[(x, y)]) for x in range_x) for y in range_y))


def get_input_intcode() -> List[int]:
    return list(map(int, get_input().split(',')))


class IntCode:
    """ A basic class to execute intcode. Developed over day 2, 5, 7, and 9 """

    def __init__(self, values: List[int], inputs: List[int] = None, input_default: bool = False, input_default_value: int = -1):
        if inputs is None:
            inputs = []
        self.code: DefaultDict[int, int] = defaultdict(int, [(i, values[i]) for i in range(len(values))])
        self.pointer: int = 0
        self.inputs: List[int] = inputs
        self.outputs: List[int] = []
        self.input_default: bool = input_default
        self.input_default_value: int = input_default_value

        self.running = True
        self.paused = False
        self.polling = False
        self.rel_base = 0
        self.pos_flags = [0, 0, 0]

    def tick(self):
        # Calculate all instruction flags
        inst = self.code[self.pointer]
        opcode = inst % 100
        self.pos_flags = [(inst // 100) % 10, (inst // 1000) % 10, (inst // 10000) % 10]

        self.paused = False
        if opcode == 1:
            self.code[self.addr(3)] = self.arg(1) + self.arg(2)
            self.pointer += 4
        elif opcode == 2:
            self.code[self.addr(3)] = self.arg(1) * self.arg(2)
            self.pointer += 4
        elif opcode == 3:
            if len(self.inputs) > 0:
                self.code[self.addr(1)] = self.inputs.pop(0)
                self.pointer += 2
                self.polling = False
            elif self.input_default:
                self.code[self.addr(1)] = self.input_default_value
                self.pointer += 2
                self.polling = True
            else:
                self.paused = True
        elif opcode == 4:
            self.outputs.append(self.arg(1))
            self.pointer += 2
            self.polling = False
        elif opcode == 5:
            if self.arg(1) != 0:
                self.pointer = self.arg(2)
            else:
                self.pointer += 3
        elif opcode == 6:
            if self.arg(1) == 0:
                self.pointer = self.arg(2)
            else:
                self.pointer += 3
        elif opcode == 7:
            self.code[self.addr(3)] = 1 if self.arg(1) < self.arg(2) else 0
            self.pointer += 4
        elif opcode == 8:
            self.code[self.addr(3)] = 1 if self.arg(1) == self.arg(2) else 0
            self.pointer += 4
        elif opcode == 9:
            self.rel_base += self.arg(1)
            self.pointer += 2
        elif opcode == 99:
            self.running = False

    def run(self):
        """ Runs until paused """
        self.paused = False
        while not self.paused and self.running:
            self.tick()
        return self

    def asciz(self, s: str):
        for c in s + '\n':
            self.inputs.append(ord(c))

    def arg(self, i: int) -> int:
        """ Internal function to get an argument, after opcode / position flags have been calculated
        :param i: the index of the argument to get, as an offset from the opcode
        :return: the argument value (immediate, positional, or relative)
        """
        if self.pos_flags[i - 1] == 0:
            return self.code[self.code[self.pointer + i]]
        elif self.pos_flags[i - 1] == 1:
            return self.code[self.pointer + i]
        elif self.pos_flags[i - 1] == 2:
            return self.code[self.rel_base + self.code[self.pointer + i]]
        raise ValueError('Unknown argument mode %d' % self.pos_flags[i - 1])

    def addr(self, i: int) -> int:
        """ Internal function to get an address, after opcode / position flags have been calculated
        :param i: the index of the address to get, as an offset from the opcode
        :return: the address (positional, or relative, addresses can't be immediate)
        """
        if self.pos_flags[i - 1] == 0:
            return self.code[self.pointer + i]
        elif self.pos_flags[i - 1] == 1:
            raise ValueError('Tried to get address with immediate argument mode')
        elif self.pos_flags[i - 1] == 2:
            return self.rel_base + self.code[self.pointer + i]
        raise ValueError('Unknown argument mode %d' % self.pos_flags[i - 1])

