import math
from collections import defaultdict


def learn_reactions(data):
    def parse_chem(chem):
        quant, name = chem.strip(" ").split(" ")
        return int(quant), name

    reactions = {}
    for line in data:
        reactants, products = line.strip("\n").split("=>")
        product_quant, product_name = parse_chem(products)
        processed_reactants = [
            parse_chem(chem) for chem in reactants.split(", ")
        ]
        reactions[product_name] = (product_quant, processed_reactants)
    return reactions


def find_ore_required(reactions, product, desired_quantity, stock):
    if product == "ORE":
        return desired_quantity

    product_available = min(stock[product], desired_quantity)
    stock[product] -= product_available
    desired_quantity -= product_available

    if desired_quantity == 0:
        return 0

    produced_per, reactants = reactions[product]
    num_reactions = math.ceil(desired_quantity / produced_per)
    ore_required = 0
    for quant, reactant in reactants:
        ore_required += find_ore_required(
            reactions, reactant, quant * num_reactions, stock)

    leftover_product = num_reactions * produced_per - desired_quantity
    stock[product] += leftover_product

    return ore_required


def find_max_fuel(available_ore, reactions):
    def check_ore_needed(fuel):
        return find_ore_required(
            reactions, "FUEL", fuel, defaultdict(lambda: 0))

    lower_bound = math.floor(available_ore / check_ore_needed(1))
    upper_bound = lower_bound * 2
    while check_ore_needed(upper_bound) < available_ore:
        upper_bound *= 2

    while upper_bound != lower_bound + 1:
        mid = math.floor((lower_bound + upper_bound) / 2)
        if check_ore_needed(mid) <= available_ore:
            lower_bound = mid
        else:
            upper_bound = mid

    return lower_bound


if __name__ == "__main__":
    with open("../input/day14.txt") as f:
        print(find_max_fuel(1e12, learn_reactions(f.readlines())))
