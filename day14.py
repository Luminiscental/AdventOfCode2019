"""AdventOfCode2019 - Day 14"""
import math
import collections
import functools

Term = collections.namedtuple("Term", "count name")
Reaction = collections.namedtuple("Reaction", "reactants product")


def parse(puzzle_input):
    """Parse the puzzle input into a dict of reaction output to reaction info."""

    def parse_term(term_string):
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
    """Return the minimum ore needed to make the given amount of fuel given the reaction dict."""

    @functools.lru_cache()  # memoization not necessary but gives a nice speed up
    def could_need(reactant, product):
        if product == "ORE":
            return False
        prod_reactants = [reactant.name for reactant in reactions[product].reactants]
        return reactant in prod_reactants or any(
            could_need(reactant, prod_reactant) for prod_reactant in prod_reactants
        )

    # apply reactions backwards until we are left with an amount of ore
    requirements = {"FUEL": for_fuel}
    while not all(req == "ORE" for req in requirements):
        # the intersection of what we can make with what we want
        reducables = reactions.keys() & requirements.keys()
        for product in reducables:
            # only reduce a term if we know we won't need more of it later
            # this is the crucial minimizing step
            if any(could_need(product, req) for req in requirements):
                continue
            # apply the reaction backwards to update our requirements
            reaction = reactions[product]
            req_count = requirements.pop(product)
            out_count = reaction.product.count
            repeats = int(math.ceil(req_count / out_count))
            for reactant in reaction.reactants:
                requirements.setdefault(reactant.name, 0)
                requirements[reactant.name] += reactant.count * repeats
    return requirements["ORE"]


def part1(reactions):
    """Solve for the answer to part 1."""
    return minimum_ore(reactions, for_fuel=1)


def part2(reactions):
    """Solve for the answer to part 2."""
    initial_ore = 1000000000000
    # get an amount of fuel we can't make
    fuel = 1
    while minimum_ore(reactions, fuel) <= initial_ore:
        fuel *= 2
    # do a binary search to find the maximum makeable fuel amount
    lower_bound = fuel // 2  # can make this much
    upper_bound = fuel  # can't make this much
    while upper_bound - lower_bound > 1:
        # the midpoint is either an improved upper bound or an improved lower bound
        mid_fuel_amount = (lower_bound + upper_bound) // 2
        mid_ore_requirement = minimum_ore(reactions, mid_fuel_amount)
        if mid_ore_requirement <= initial_ore:
            lower_bound = mid_fuel_amount
        else:
            upper_bound = mid_fuel_amount
    return lower_bound
