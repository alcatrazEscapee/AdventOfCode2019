# Day 11: Space Police

from utils import *
from collections import defaultdict


def main(values):
    panels = defaultdict(int)  # 0 = black, 1 = white
    painted_once = set()
    code = IntCode(values, [])

    robot = (0, 0)
    robot_dir = (0, 1)  # UP

    # For part 2, the robot starts on a white tile
    panels[robot] = 1

    while code.running:
        code.inputs.append(panels[robot])
        code.run_until()
        if code.running:
            panels[robot] = code.outputs.pop(0)
            painted_once.add(robot)

            turn = code.outputs.pop(0)
            if turn == 0:
                robot_dir = tuple(protccw(robot_dir))
            elif turn == 1:
                robot_dir = tuple(protcw(robot_dir))
            robot = tuple(padd(robot, robot_dir))

    print('Part 1:', len(painted_once))

    min_x, max_x = min_max([p[0] for p in panels.keys()])
    min_y, max_y = min_max([p[1] for p in panels.keys()])

    print('Part 2:')
    print('\n'.join(''.join({1: '\u2591\u2591', 0: '  '}[panels[(x, y)]] for x in range(min_x, 1 + max_x)) for y in range(min_y, 1 + max_y)))


if __name__ == '__main__':
    main([*ints(get_input())])
