"""
AdventOfCode2019 - Day 14
"""

import math
import collections
import functools

Term = collections.namedtuple("Term", "count name")
Reaction = collections.namedtuple("Reaction", "reactants product")


def parse(puzzle_input):
    """
    Parse the puzzle input into a dict of reaction output name to reaction info.
    """

    def parse_term(term_string):
        """
        Parse a string like "12 X" into a term value.
        """
        count_str, name_str = term_string.split()
        return Term(int(count_str), name_str)

    reactions = {}
    for line in puzzle_input.splitlines():
        lhs, rhs = line.split("=>")
        reactants = [parse_term(reactant_term) for reactant_term in lhs.split(",")]
        product = parse_term(rhs)
        reaction = Reaction(reactants, product)
        reactions[reaction.product.name] = reaction
    return reactions


def minimum_ore(reactions, for_fuel):
    """
    Return the minimum ore needed to make the given amount of fuel given the reaction dict.
    """

    # not necessary to memoize but a nice speed up
    @functools.lru_cache()
    def made_from(reactant, product):
        if product == "ORE":
            return False
        prod_reactants = [reactant.name for reactant in reactions[product].reactants]
        return reactant in prod_reactants or any(
            made_from(reactant, prod_reactant) for prod_reactant in prod_reactants
        )

    requirements = {"FUEL": for_fuel}
    while not all(req == "ORE" for req in requirements):
        reducables = reactions.keys() & requirements.keys()
        for product in reducables:
            if any(made_from(product, req) for req in requirements):
                continue
            reaction = reactions[product]
            req_count = requirements.pop(product)
            out_count = reaction.product.count
            repeats = int(math.ceil(req_count / out_count))
            for reactant in reaction.reactants:
                requirements.setdefault(reactant.name, 0)
                requirements[reactant.name] += reactant.count * repeats

    return requirements["ORE"]


def part1(reactions):
    """
    Solve for the answer to part 1.
    """
    return minimum_ore(reactions, for_fuel=1)


def part2(reactions):
    """
    Solve for the answer to part 2.
    """
    initial_ore = 1000000000000

    # get a bound
    fuel = 1
    while minimum_ore(reactions, fuel) <= initial_ore:
        fuel *= 2

    # use bisection
    lower_bound = fuel // 2
    upper_bound = fuel
    while upper_bound - lower_bound > 1:
        mid_fuel = (lower_bound + upper_bound) // 2
        mid_ore = minimum_ore(reactions, mid_fuel)
        if mid_ore <= initial_ore:
            lower_bound = mid_fuel
        else:
            upper_bound = mid_fuel
    return lower_bound
