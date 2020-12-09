# Day 25: Cryostasis
# 50 Stars!!! Total Score: 1054, Rank: 68th

from utils import *
from typing import Tuple, List
from re import findall
from itertools import combinations, chain


def play(runner: IntCode):
    # Interactive mode!
    cmd = ''
    while cmd != 'exit' and runner.running:
        if cmd != '':
            for c in cmd + '\n':
                runner.inputs.append(ord(c))

        runner.run()
        print(''.join(chr(c) for c in runner.outputs))
        runner.outputs.clear()

        cmd = input('>').replace('\\n', '\n')


def explore(code: List[int]):
    locations = {}
    paths = [tuple()]
    while paths:
        path = paths.pop(0)
        for step in ('north', 'east', 'west', 'south'):
            runner = IntCode(code)
            for d in path:
                for c in d + '\n':
                    runner.inputs.append(ord(c))
            runner.run()
            runner.outputs.clear()
            for c in step + '\n':
                runner.inputs.append(ord(c))
            runner.run()
            output_text = ''.join(chr(c) for c in runner.outputs)
            if 'You can\'t go that way' not in output_text:
                room_name = findall('== (.*) ==', output_text)[0]
                if room_name not in locations:
                    full_path = (*path, step)
                    paths.append(full_path)
                    items = findall('Items here:[.\n]*- (.*)', output_text)
                    desc = findall('==\n(.*)', output_text)[0]
                    locations[room_name] = desc, items, full_path
    for k, v in locations.items():
        print(k, ':')
        for i in v:
            print('\t', i)


def checkpoint(runner: IntCode, items: List[str]):
    # dump all items initially
    for item in items:
        runner.asciz('drop ' + item)
    runner.run()
    for combo in chain.from_iterable(combinations(items, n) for n in range(len(items) + 1)):
        for item in combo:
            runner.asciz('take ' + item)
        runner.run()
        runner.outputs.clear()
        runner.asciz('south')
        runner.run()
        output_text = ''.join(chr(c) for c in runner.outputs)
        if 'Analysis complete! You may proceed.' in output_text:
            print('required: ', combo)
            return
        for item in combo:
            runner.asciz('drop ' + item)


if __name__ == '__main__':
    # Instructions were figured out by playing this by hand, and via use of the explore and checkpoint functions!
    droid = IntCode(get_input_intcode())
    droid.asciz('\n'.join(['south', 'west', 'take hologram', 'south', 'west', 'west', 'take hypercube', 'east', 'east', 'north', 'east', 'south', 'take cake', 'west', 'north', 'take coin', 'south', 'east', 'east', 'south', 'east', 'south', 'south']))
    droid.run()
    print('Part 1:', ints(''.join(chr(c) for c in droid.outputs))[0])
