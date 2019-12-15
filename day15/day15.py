# Day 15: Oxygen System
# Rank 28 / 74


from utils import *
from collections import defaultdict


def main(code):
    droid = IntCode(code)

    found = {(0, 0)}
    paths = [[0, 0, '']]
    grid = defaultdict(lambda: '#')
    path_to_o2 = None

    # This BFS is not the most efficient (due to the nature of moving the droid back and forth a lot)
    while paths:
        x, y, path = paths.pop(0)

        # move the droid to that path
        for move in path:
            droid.inputs.append(DROID[move])
        droid.run()
        droid.outputs.clear()

        # test all possible paths
        for d in 'NESW':
            new_path = path + d
            # move one in that direction
            droid.inputs.append(DROID[d])
            droid.outputs.clear()
            droid.run()

            ret_code = droid.outputs.pop(0)
            x1, y1 = padd((x, y), MOVE[d])
            if ret_code == 0:
                # no movement, invalid path. Mark the wall and continue
                pass
            else:
                assert ret_code == 1 or ret_code == 2, 'Invalid ret_code %d' % ret_code

                if ret_code == 2:
                    grid[(x1, y1)] = 'O'
                    path_to_o2 = x1, y1, new_path
                else:
                    grid[(x1, y1)] = '.'

                # valid path. Mark the new path and walk one step back
                if (x1, y1) not in found:
                    found.add((x1, y1))
                    paths.append([x1, y1, new_path])

                droid.inputs.append(DROID[INVERSE[d]])
                droid.run()

        # move the droid back to start
        for move in path[::-1]:
            droid.inputs.append(DROID[INVERSE[move]])
        droid.run()
        droid.outputs.clear()

    print_grid(grid, padding=1)
    print('Part 1:', len(path_to_o2[2]), 'Steps')

    print('Running Part 2')
    minutes = 0
    while True:
        new_tiles = set()
        for pos, value in grid.items():
            if value == '.':
                for d in MOVE.values():
                    loc = tuple(padd(d, pos))
                    if grid[loc] == 'O':
                        new_tiles.add(pos)
        # add the new tiles in a batch
        for tile in new_tiles:
            grid[tile] = 'O'
        if len(new_tiles) == 0:
            break
        minutes += 1

    print('Part 2:', minutes, 'Minutes')


DROID = {'N': 1, 'S': 2, 'W': 3, 'E': 4}
MOVE = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
INVERSE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

if __name__ == '__main__':
    main(get_input_intcode())
