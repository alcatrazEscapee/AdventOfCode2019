# Day 23: Category Six
# Rank: 109 / 80

from utils import *


def main(values):
    block = [IntCode(values, [i], input_default=True) for i in range(50)]
    nat = (0, 0)
    nat_delivered = set()
    part1 = False

    while any(b.running for b in block):
        for runner in block:
            runner.tick()
            while len(runner.outputs) > 2:
                addr = runner.outputs.pop(0)
                x = runner.outputs.pop(0)
                y = runner.outputs.pop(0)
                if addr == 255:
                    nat = x, y
                    if part1:
                        part1 = True
                        print('Part 1:', y)
                else:
                    block[addr].inputs.append(x)
                    block[addr].inputs.append(y)
        if all(r.polling for r in block):
            print('nat active', nat)
            for r in block:
                r.polling = False
            block[0].inputs.append(nat[0])
            block[0].inputs.append(nat[1])
            if nat[1] not in nat_delivered:
                nat_delivered.add(nat[1])
            else:
                print('Part 2:', nat[1])
                break


if __name__ == '__main__':
    main(get_input_intcode())
