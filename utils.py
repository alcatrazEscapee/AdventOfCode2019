from re import findall
from typing import Iterable
from collections import defaultdict
from functools import reduce
from math import gcd


# Input Reading
def get_input() -> str:
    with open('./input.txt') as f:
        return f.read()


def get_input_lines() -> list:
    return get_input().split('\n')


def ints(text: str) -> tuple:
    return tuple(map(int, findall('([\-+]?\d+)', text)))


def flat_map(collection: Iterable):
    for container in collection:
        for element in container:
            yield element


# Geometry
def padd(x: Iterable, y: Iterable) -> list:
    return [a + b for a, b in zip(x, y)]


def psub(x: Iterable, y: Iterable) -> list:
    return [a - b for a, b in zip(x, y)]


def pmul(x: Iterable, a: float) -> list:
    return [a * y for y in x]


def pdot(x: Iterable, y: Iterable) -> list:
    return sum(a * b for a, b in zip(x, y))


def pnorm1(x: Iterable, y: Iterable = None) -> float:
    if y is not None:
        x = psub(x, y)
    return sum(map(abs, x))


def pnorm2sq(x: Iterable, y: Iterable = None) -> float:
    if y is not None:
        x = psub(x, y)
    return sum(i * i for i in x)


def protccw(x) -> list:
    return [-x[1], x[0]]


def protcw(x) -> list:
    return [x[1], -x[0]]


def psign(x: Iterable) -> list:
    return [(0 if y == 0 else (1 if y > 0 else -1)) for y in x]


def pabs(x: Iterable) -> list:
    return [abs(y) for y in x]


def min_max(x: Iterable) -> tuple:
    return min(x), max(x)


def lcm(a: int, b: int) -> int:
    """ Return lowest common multiple. """
    return a * b // gcd(a, b)


def gcd_iter(sequence: Iterable) -> int:
    """ Return greatest common divisor of a list """
    return reduce(gcd, sequence)


def lcm_iter(sequence: Iterable) -> int:
    return reduce(lcm, sequence)


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


class IntCode:
    """ A basic class to execute intcode. Developed over day 2, 5, 7, and 9 """

    def __init__(self, values: list, inputs: list):
        self.code = defaultdict(int, [(i, values[i]) for i in range(len(values))])
        self.pointer = 0
        self.inputs = inputs
        self.outputs = []
        self.running = True
        self.paused = False
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
            else:
                self.paused = True
        elif opcode == 4:
            self.outputs.append(self.arg(1))
            self.pointer += 2
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
        while self.running:
            self.tick()
        return self

    def run_until(self):
        """ Runs until paused """
        self.paused = False
        while not self.paused and self.running:
            self.tick()
        return self

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
