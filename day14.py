"""AdventOfCode2019 - Day 14"""
import math
import collections
import functools

Term = collections.namedtuple("Term", "count name")
Reaction = collections.namedtuple("Reaction", "reactants product")


class ReactionState:
    """Class storing knowledge about possible reactions."""

    def __init__(self, reaction_dict):
        self.reactions = reaction_dict
        self.known_chemicals = self.reactions.keys()

    @functools.lru_cache(maxsize=None)
    def could_need_for(self, reactant, product):
        """Check if a product could need a reactant to make."""
        if product == "ORE":
            return False
        prod_reactants = tuple(map(lambda r: r.name, self.reactions[product].reactants))
        return reactant in prod_reactants or any(
            self.could_need_for(reactant, prod_reactant)
            for prod_reactant in prod_reactants
        )


def parse(puzzle_input):
    """Parse the puzzle input into a ReactionState instance."""

    def parse_term(term_string):
        count_str, name_str = term_string.split()
        return Term(int(count_str), name_str)

    reactions = {}
    for line in puzzle_input.splitlines():
        lhs, rhs = line.split("=>")
        reactants = tuple(parse_term(reactant_term) for reactant_term in lhs.split(","))
        product = parse_term(rhs)
        reaction = Reaction(reactants, product)
        reactions[reaction.product.name] = reaction
    return ReactionState(reactions)


def minimum_ore(reaction_state, for_fuel):
    """Return the minimum ore needed to make the given amount of fuel given the reaction dict."""

    # apply reactions backwards until we are left with an amount of ore
    requirements = {"FUEL": for_fuel}
    while not all(req == "ORE" for req in requirements):
        # the intersection of what we can make with what we want
        reducables = reaction_state.known_chemicals & requirements.keys()
        for product in reducables:
            # only reduce a term if we know we won't need more of it later
            # this is the crucial minimizing step
            if any(
                reaction_state.could_need_for(reactant=product, product=req)
                for req in requirements
            ):
                continue
            # apply the reaction backwards to update our requirements
            reaction = reaction_state.reactions[product]
            req_count = requirements.pop(product)
            out_count = reaction.product.count
            repeats = int(math.ceil(req_count / out_count))
            for reactant in reaction.reactants:
                requirements.setdefault(reactant.name, 0)
                requirements[reactant.name] += reactant.count * repeats
    return requirements["ORE"]


def part1(reaction_state):
    """Solve for the answer to part 1."""
    return minimum_ore(reaction_state, for_fuel=1)


def part2(reaction_state):
    """Solve for the answer to part 2."""
    initial_ore = 1000000000000
    # get an amount of fuel we can't make
    fuel = 1
    while minimum_ore(reaction_state, fuel) <= initial_ore:
        fuel *= 2
    # do a binary search to find the maximum makeable fuel amount
    lower_bound = fuel // 2  # can make this much
    upper_bound = fuel  # can't make this much
    while upper_bound - lower_bound > 1:
        # the midpoint is either an improved upper bound or an improved lower bound
        mid_fuel_amount = (lower_bound + upper_bound) // 2
        mid_ore_requirement = minimum_ore(reaction_state, mid_fuel_amount)
        if mid_ore_requirement <= initial_ore:
            lower_bound = mid_fuel_amount
        else:
            upper_bound = mid_fuel_amount
    return lower_bound
