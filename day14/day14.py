# Day 14: Space Stoichiometry
# Rank 86 / 99

from utils import *
from collections import defaultdict
from math import ceil
from typing import List, Tuple, Dict, Any


def main():
    recipes, raw_recipes = build_recipes(get_input_lines())
    fuel = 1
    ore = required_ore(recipes, raw_recipes, fuel)
    print('Part 1:', ore)

    ore_max = 1_000_000_000_000
    while True:
        fuel = fuel * ore_max // ore
        ore_estimate = required_ore(recipes, raw_recipes, fuel)
        if ore == ore_estimate <= ore_max:
            break
        else:
            ore = ore_estimate

    print('Part 2:', fuel)


def required_ore(recipes: Dict[Any, tuple], raw_recipes: Dict[Any, tuple], fuel_amount: int) -> int:
    inventory = defaultdict(int)
    inventory['FUEL'] = fuel_amount
    ingredients = {'FUEL'}
    raw_ingredients = set()

    while ingredients:
        item = ingredients.pop()
        count = inventory[item]
        if item in recipes:
            recipe = recipes[item]
            ratio = ceil(count / recipe[0])
            for i in range(0, len(recipe[1]), 2):
                amount = ratio * int(recipe[1][i])
                needed_item = recipe[1][i + 1]
                inventory[needed_item] += amount
                ingredients.add(needed_item)
            produced = recipe[0] * ratio
            inventory[item] -= produced
        else:
            raw_ingredients.add(item)

    ore_count = 0
    for item in raw_ingredients:
        count = inventory[item]
        if count > 0:
            recipe = raw_recipes[item]
            ratio = ceil(count / recipe[1])
            count -= recipe[1] * ratio
            ore_count += recipe[0] * ratio

    return ore_count


def build_recipes(text: List[str]) -> Tuple[Dict[Any, tuple], Dict[Any, tuple]]:
    recipes = {}
    raw_recipes = {}
    for line in text:
        ins, outs = line.split(' => ')
        ins_list = ins.replace(',', '').split(' ')
        outs_list = outs.replace(',', '').split(' ')
        if ins_list[1] == 'ORE':
            raw_recipes[outs_list[1]] = (int(ins_list[0]), int(outs_list[0]))
        else:
            recipes[outs_list[1]] = (int(outs_list[0]), ins_list)
    return recipes, raw_recipes


if __name__ == '__main__':
    main()
