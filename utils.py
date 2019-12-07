from re import findall
from collections import defaultdict


def get_input() -> str:
    with open('./input.txt') as f:
        return f.read()


def get_input_lines() -> list:
    return get_input().split('\n')


def ints(text: str) -> tuple:
    return tuple(map(int, findall('([+\-0-9]+)', text)))


def flat_map(collection):
    for container in collection:
        for element in container:
            yield element


class IntCode:
    """ A basic class to run intcode processing. Developed over day 2, 5, and 7 solutions. """

    def __init__(self, values: list, inputs: list):
        # Use a defaultdict here because then we can ignore IndexErrors
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
