import re


def get_input(day_num: int) -> str:
    with open('./../assets/day%d_input.txt' % day_num) as f:
        return f.read()


def get_input_lines(day_num: int) -> list:
    return get_input(day_num).split('\n')


def ints(text: str) -> tuple:
    return tuple(map(int, re.findall('([+\-0-9]+)', text)))


def flat_map(collection):
    for container in collection:
        for element in container:
            yield element
