"""
AdventOfCode2019 - Day 12
"""

import itertools


def parse_vector(string):
    """
    Parse a string as a 3-component vector.
    """
    string = string[1:-1]
    components = string.split(",")
    return [int(component.split("=")[-1]) for component in components]


def vector_energy(vector):
    """
    Work out the energy from a vector; the manhattan magnitude.
    """
    return sum(abs(component) for component in vector)


class Moon:
    """
    Class representing the physical state of a moon.
    """

    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def energy(self):
        """
        Calculate the energy of this moon; potential + kinetic.
        """
        return vector_energy(self.position) * vector_energy(self.velocity)

    def apply_velocity(self):
        """
        Integrate velocity for one timestep.
        """
        for i in range(3):
            self.position[i] += self.velocity[i]

    @staticmethod
    def apply_gravity(moon1, moon2):
        """
        Apply gravity to the velocity of moon1 and moon2.
        """
        for i in range(3):
            if moon1.position[i] == moon2.position[i]:
                continue
            sign = 1 if moon1.position[i] > moon2.position[i] else -1
            moon1.velocity[i] -= sign
            moon2.velocity[i] += sign

    @staticmethod
    def timestep(moons):
        """
        Apply a single timestep for a list of moons.
        """
        for moon1, moon2 in itertools.combinations(moons, 2):
            Moon.apply_gravity(moon1, moon2)
        for moon in moons:
            moon.apply_velocity()


def parse(puzzle_input):
    """
    Parse the puzzle input.
    """
    return [Moon(parse_vector(line)) for line in puzzle_input.splitlines()]


def part1(moons):
    """
    Solve for the answer to part 1.
    """
    for _ in range(1000):
        Moon.timestep(moons)
    return sum(moon.energy() for moon in moons)


def part2(moons):
    """
    Solve for the answer to part 2.
    """
