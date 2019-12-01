import re


def read(day_num: int) -> str:
    with open('./../assets/day%d_input.txt' % day_num) as f:
        return f.read()


def ints(text: str) -> tuple:
    return tuple(map(int, re.findall('([+\-0-9]+)', text)))
