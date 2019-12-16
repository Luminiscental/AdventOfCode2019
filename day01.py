"""AdventOfCode2019 - Day 1"""
import functools


@functools.lru_cache(maxsize=None)
def fuel_from_mass1(mass):
    """Calculate the required fuel for a module based on its mass."""
    return mass // 3 - 2


def fuel_from_mass2(mass):
    """Calculate the required fuel for a module based on its mass accounting for fuel mass."""
    result = 0
    fuel = fuel_from_mass1(mass)
    while fuel > 0:
        result = result + fuel
        fuel = fuel_from_mass1(fuel)
    return result


def parse(puzzle_input):
    """Parse the input into a list of masses."""
    return [int(line) for line in puzzle_input.splitlines()]


def part1(masses):
    """Solve for the answer to part 1."""
    return sum(fuel_from_mass1(mass) for mass in masses)


def part2(masses):
    """Solve for the answer to part 2."""
    return sum(fuel_from_mass2(mass) for mass in masses)
