# Day 12: The N-Body Problem

from utils import *


def find_energy(moons_pos):
    moons_pos = moons_pos[:]
    moons_vel = [[0] * 3 for _ in range(4)]
    for _ in range(1000):
        tick(moons_pos, moons_vel)

    pe = [pnorm1(p) for p in moons_pos]
    ke = [pnorm1(p) for p in moons_vel]
    print('Part 1', sum(pe[i] * ke[i] for i in range(4)))


def tick(moons_pos, moons_vel):
    for i in range(4):  # moon to be moved
        for j in range(4):  # moon to be checked against
            moons_vel[i] = padd(moons_vel[i], psign(psub(moons_pos[j], moons_pos[i])))

    for i in range(4):
        moons_pos[i] = padd(moons_pos[i], moons_vel[i])


def find_cycle(moons_pos: list):
    moons_pos = moons_pos[:]
    initial_states = [(tuple(moons_pos[i][j] for i in range(4)), (0, 0, 0, 0)) for j in range(3)]
    moons_vel = [(0, 0, 0)] * 4
    min_cycle = [0] * 3
    found_cycle = [False] * 3
    t = 0
    while not all(found_cycle):
        tick(moons_pos, moons_vel)
        if t % 10000 == 0:
            print('Tick', min_cycle)
        t += 1
        for i in range(3):
            if not found_cycle[i]:
                min_cycle[i] += 1
                state = tuple(moons_pos[j][i] for j in range(4)), tuple(moons_vel[k][i] for k in range(4))
                if state == initial_states[i]:
                    found_cycle[i] = True
    print('Part 2:', lcm_iter(min_cycle))


if __name__ == '__main__':
    puzzle_input = list(map(ints, get_input_lines()))
    find_energy(puzzle_input)
    find_cycle(puzzle_input)
