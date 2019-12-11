# Day 8: Sensor Boost
# Rank 61 / 61


from utils import *


if __name__ == '__main__':
    # All actual code was written in util today!
    code = [*ints(get_input())]
    print('Part 1:', IntCode(code, [1]).run().outputs[0])
    print('Part 2:', IntCode(code, [2]).run().outputs[0])
