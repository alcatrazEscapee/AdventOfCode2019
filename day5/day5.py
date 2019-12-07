# Day 5: Sunny with a Chance of Asteroids

from utils import *


def run(values: list, inputs: list) -> list:
    # Solution has been modified to use the IntCode class from later solutions
    return IntCode(values, inputs).run().outputs


if __name__ == '__main__':
    assert run([3, 0, 4, 0, 99], [123]) == [123]
    assert run([1002, 4, 3, 4, 33], []) == []
    assert run([1101, 100, -1, 4, 0], []) == []
    assert run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [1]) == [0]
    assert run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]) == [1]
    assert run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [1]) == [1]
    assert run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8]) == [0]
    assert run([3, 3, 1108, -1, 8, 3, 4, 3, 99], [1]) == [0]
    assert run([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]) == [1]
    assert run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [1]) == [1]
    assert run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8]) == [0]
    assert run([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [123]) == [1]
    assert run([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]) == [0]
    assert run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [123]) == [1]
    assert run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]) == [0]

    code = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    assert run(code, [7]) == [999]
    assert run(code, [8]) == [1000]
    assert run(code, [9]) == [1001]

    input_code = [*ints(get_input())]
    print('Part 1:', run(input_code, [1])[-1])
    print('Part 2:', run(input_code, [5])[0])
