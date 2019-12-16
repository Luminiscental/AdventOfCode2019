"""AdventOfCode2019 - Day 12"""
import collections
import copy
import itertools
import re
import multiprocessing
import functools
from util import sign, lcm_all

Moon = collections.namedtuple("Moon", "pos vel")


def parse_vector(string):
    """Parse a vector from a string (not robust)."""
    return list(map(int, re.findall(r"-?\d+", string)))


def energy(moon):
    """Calculate the energy of a moon."""

    def vector_energy(vector):
        return sum(abs(component) for component in vector)

    return vector_energy(moon.pos) * vector_energy(moon.vel)


def step(moons, axis):
    """Apply a timestep to the system in a given axis."""
    for moon1, moon2 in itertools.combinations(moons, 2):
        # apply gravity
        to_moon1 = sign(moon1.pos[axis] - moon2.pos[axis])
        moon1.vel[axis] -= to_moon1
        moon2.vel[axis] += to_moon1
    for moon in moons:
        # apply velocity
        moon.pos[axis] += moon.vel[axis]


def state_tuple(moons, axis):
    """Get a tuple encoding the state of the system in a given axis."""
    return tuple((moon.pos[axis], moon.vel[axis]) for moon in moons)


def parse(puzzle_input):
    """Parse the puzzle input into a list of moons."""
    return [
        Moon(pos=parse_vector(line), vel=[0, 0, 0])
        for line in puzzle_input.splitlines()
    ]


def part1(moons):
    """Solve for the answer to part 1."""
    sim = copy.deepcopy(moons)
    for _ in range(1000):
        for axis in range(3):
            step(sim, axis)
    return sum(map(energy, sim))


def find_period(moons, initial_states, axis):
    """Find the period of the system in a given axis.
    Since the time step is invertible, the first repeat will be the initial state."""
    sim = copy.deepcopy(moons)
    steps = 0
    step(sim, axis)
    steps += 1
    while state_tuple(sim, axis) != initial_states[axis]:
        step(sim, axis)
        steps += 1
    return steps


def part2(moons):
    """Solve for the answer to part 2."""
    initial_states = [state_tuple(moons, axis) for axis in range(3)]
    period_finder = functools.partial(find_period, moons, initial_states)
    with multiprocessing.Pool(3) as pool:
        periods = pool.map(period_finder, range(3))
    # The overall period is the lcm of the period of the individual component systems.
    return lcm_all(periods)
