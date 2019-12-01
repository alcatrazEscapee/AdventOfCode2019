from src.utils import *


def main():
    modules = ints(read(1))
    print('Part 1:', sum([d // 3 - 2 for d in modules]))

    total = 0
    for module in modules:
        mass = 0
        fuel = module // 3 - 2
        while fuel > 0:
            mass += fuel
            fuel = fuel // 3 - 2
        total += mass

    print('Part 2:', total)


if __name__ == '__main__':
    main()
