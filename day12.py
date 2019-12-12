"""
AdventOfCode2019 - Day 12
"""

import itertools
import math
import functools


def lcm(numbers):
    """
    Return the lowest common multiple of a sequence of numbers.
    """

    def lcm2(num1, num2):
        """
        Return the lowest common multiple of 2 numbers.
        """
        return num1 * num2 // math.gcd(num1, num2)

    return functools.reduce(lcm2, numbers)


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

    def copy(self):
        """
        Construct a new moon with the same state as self.
        """
        result = Moon(self.position.copy())
        result.velocity = self.velocity.copy()
        return result

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

    @staticmethod
    def get_state(moons, component):
        """
        Return the state of the system in a given component.
        """
        return tuple(
            (moon.position[component], moon.velocity[component]) for moon in moons
        )


def parse(puzzle_input):
    """
    Parse the puzzle input.
    """
    return [Moon(parse_vector(line)) for line in puzzle_input.splitlines()]


def part1(moons):
    """
    Solve for the answer to part 1.
    """
    sim = [moon.copy() for moon in moons]
    for _ in range(1000):
        Moon.timestep(sim)
    return sum(moon.energy() for moon in sim)


def part2(moons):
    """
    Solve for the answer to part 2.
    """
    initial_states = {i: Moon.get_state(moons, i) for i in range(3)}
    periods = [0, 0, 0]
    for i in range(3):
        sim = [moon.copy() for moon in moons]
        steps = 0

        Moon.timestep(sim)
        steps += 1
        while Moon.get_state(sim, i) != initial_states[i]:
            Moon.timestep(sim)
            steps += 1

        periods[i] = steps
    return lcm(periods)
