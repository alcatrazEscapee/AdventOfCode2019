# Day 7: Amplification Circuit
# Leaderboard 36 / 25

from utils import *
from collections import defaultdict
from itertools import permutations


class IntCode:
    """ A basic class to run intcode processing. Main routine copied from day 5 """

    def __init__(self, values: list, inputs: list):
        self.code = defaultdict(int, [(i, values[i]) for i in range(len(values))])
        self.pointer = 0
        self.inputs = inputs
        self.outputs = []
        self.running = True
        self.paused = False

    def tick(self):
        opcode = self.code[self.pointer] % 100
        pos1 = ((self.code[self.pointer] // 100) % 10) == 0
        pos2 = ((self.code[self.pointer] // 1000) % 10) == 0
        # pos3 = ((self.code[self.pointer] // 10000) % 10) == 0

        arg1 = self.code[self.code[self.pointer + 1]] if pos1 else self.code[self.pointer + 1]
        arg2 = self.code[self.code[self.pointer + 2]] if pos2 else self.code[self.pointer + 2]
        # arg3 = code[code[pointer + 3]] if pos3 else code[pointer + 3]

        self.paused = False
        if opcode == 1:
            self.code[self.code[self.pointer + 3]] = arg1 + arg2
            self.pointer += 4
        elif opcode == 2:
            self.code[self.code[self.pointer + 3]] = arg1 * arg2
            self.pointer += 4
        elif opcode == 3:
            if len(self.inputs) > 0:
                self.code[self.code[self.pointer + 1]] = self.inputs.pop(0)
                self.pointer += 2
            else:
                self.paused = True
        elif opcode == 4:
            self.outputs.append(arg1)
            self.pointer += 2
        elif opcode == 5:
            if arg1 != 0:
                self.pointer = arg2
            else:
                self.pointer += 3
        elif opcode == 6:
            if arg1 == 0:
                self.pointer = arg2
            else:
                self.pointer += 3
        elif opcode == 7:
            self.code[self.code[self.pointer + 3]] = 1 if arg1 < arg2 else 0
            self.pointer += 4
        elif opcode == 8:
            self.code[self.code[self.pointer + 3]] = 1 if arg1 == arg2 else 0
            self.pointer += 4
        elif opcode == 99:
            self.running = False

    def run(self):
        while self.running:
            self.tick()
        return self


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
                a.tick()

        values.add(amplifiers[4].outputs[0])

    print('Part 2:', max(values))


if __name__ == '__main__':
    input_code = [*ints(get_input())]
    part1(input_code)
    part2(input_code)
