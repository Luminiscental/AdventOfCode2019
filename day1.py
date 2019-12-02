"""
AdventOfCode2019 - Day 1
"""

import util

PUZZLE_INPUT = [int(line) for line in util.get_input(1).splitlines()]


def fuel_from_mass1(mass):
    """
    Calculate the required fuel for a module based on its mass.
    """
    return mass // 3 - 2


def fuel_from_mass2(mass):
    """
    Calculate the required fuel for a module
    """
    result = 0
    fuel = fuel_from_mass1(mass)

    while fuel > 0:
        result = result + fuel
        fuel = fuel_from_mass1(fuel)

    return result


def part1(masses):
    """
    Solve for the answer to part 1.
    """
    return sum(fuel_from_mass1(mass) for mass in masses)


def part2(masses):
    """
    Solve for the answer to part 2.
    """
    return sum(fuel_from_mass2(mass) for mass in masses)


if __name__ == "__main__":
    print(f"part1: {part1(PUZZLE_INPUT)}")
    print(f"part2: {part2(PUZZLE_INPUT)}")
