"""
AdventOfCode2019 - Day 1
"""

import util


PUZZLE_INPUT = util.get_input(1)


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


def run():
    """
    Solve and display the answer.
    """
    masses = [int(line) for line in PUZZLE_INPUT.splitlines()]
    fuel1 = sum(fuel_from_mass1(mass) for mass in masses)
    fuel2 = sum(fuel_from_mass2(mass) for mass in masses)
    print(f"part1: {fuel1}")
    print(f"part2: {fuel2}")


if __name__ == "__main__":
    run()
