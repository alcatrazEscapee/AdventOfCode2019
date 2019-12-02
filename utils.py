import re


def get_input() -> str:
    with open('./input.txt') as f:
        return f.read()


def get_input_lines() -> list:
    return get_input().split('\n')


def ints(text: str) -> tuple:
    return tuple(map(int, re.findall('([+\-0-9]+)', text)))


def flat_map(collection):
    for container in collection:
        for element in container:
            yield element
