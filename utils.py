from re import findall
from typing import Iterable, Dict, Any, Tuple, List, TypeVar
from collections import defaultdict
from functools import reduce
from math import gcd

Number = TypeVar('Number', int, float)


# Input Reading
def get_input(path: str = './input.txt') -> str:
    with open(path) as f:
        return f.read()


def get_input_lines(path: str = './input.txt') -> List[str]:
    return get_input(path).split('\n')


def get_input_intcode() -> List[int]:
    return [*ints(get_input())]


def ints(text: str) -> Tuple[int]:
    return tuple(map(int, findall('([\-+]?\d+)', text)))


# Geometry
def padd(x: Iterable[Number], y: Iterable[Number]) -> List[Number]:
    return [a + b for a, b in zip(x, y)]


def psub(x: Iterable[Number], y: Iterable[Number]) -> List[Number]:
    return [a - b for a, b in zip(x, y)]


def pmul(x: Iterable[Number], a: Number) -> List[Number]:
    return [a * y for y in x]


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


def protccw(x: List[Number]) -> List[Number]:
    return [-x[1], x[0]]


def protcw(x: List[Number]) -> List[Number]:
    return [x[1], -x[0]]


def psign(x: Iterable[Number]) -> List[Number]:
    return [sign(y) for y in x]


def pabs(x: Iterable[Number]) -> List[Number]:
    return [abs(y) for y in x]


def print_grid(grid_objects: Dict[Tuple[int, int], Any], values_map: Dict[Any, str] or None = None, padding: int = 0, reverse_y: bool = False, reverse_x: bool = False):
    """ Prints a grid, represented as a map from points to values, to the console. Default is top right = positive x, y """
    def pixel(p: Any) -> str:
        if values_map is None:
            return str(p)
        else:
            return values_map[p] if p in values_map else '?'

    min_x, max_x = min_max([p[0] for p in grid_objects.keys()])
    min_y, max_y = min_max([p[1] for p in grid_objects.keys()])
    min_x -= padding
    min_y -= padding
    max_x += padding
    max_y += padding
    range_x = range(max_x, min_x - 1, -1) if reverse_x else range(min_x, max_x + 1)
    range_y = range(min_y, max_y + 1) if reverse_y else range(max_y, min_y - 1, -1)

    print('\n'.join(''.join(pixel(grid_objects[(x, y)]) for x in range_x) for y in range_y))


def min_max(x: Iterable[Number]) -> Tuple[Number, Number]:
    return min(x), max(x)


def sign(a: Number) -> Number:
    return 0 if a == 0 else (-1 if a < 0 else 1)


def lcm(a: int, b: int) -> int:
    """ Return lowest common multiple. """
    return a * b // gcd(a, b)


def gcd_iter(sequence: Iterable[int]) -> int:
    """ Return greatest common divisor of a list """
    return reduce(gcd, sequence)


def lcm_iter(sequence: Iterable[int]) -> int:
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


def bin_search(low: int, high: int, target: int, data) -> int:
    while low < high:
        mid = (low + high + 1) // 2
        if data(mid) <= target:
            low = mid
        else:
            high = mid - 1
    return low


class IntCode:
    """ A basic class to execute intcode. Developed over day 2, 5, 7, and 9 """

    def __init__(self, values: List[int], inputs: List[int] = None):
        if inputs is None:
            inputs = []
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
