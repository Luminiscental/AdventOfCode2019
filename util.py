"""
General utility functions for all days.
"""

import sys
import time
import importlib
import contextlib
import inspect
import math
import functools

import requests


def get_input(day_number):
    """
    Get the puzzle input for the given day.
    """
    try:
        with open(".cookie", "r") as cookie_file:
            cookie = cookie_file.read().strip()
            return requests.get(
                f"https://adventofcode.com/2019/day/{day_number}/input",
                cookies={"session": cookie},
            ).text
    except FileNotFoundError:
        print(
            "Could not find .cookie file to get input from adventofcode.com, "
            "input is user-dependent so I need your session id"
        )
        sys.exit(1)


@contextlib.contextmanager
def timer(desc):
    """
    Context manager for timing a block of code once.
    """
    start = time.time()
    yield
    end = time.time()
    print(f"{desc}: took {end - start:0.5f} seconds")


def apply_trim_args(func, *args):
    """
    Apply a function to given arguments, using only as many as required.
    """
    arg_count = len(inspect.signature(func).parameters)
    return func(*args[:arg_count])


def run_day(day_num):
    """
    Solve and print the answer for a given day.
    """
    puzzle_input = get_input(day_num)
    day_module = importlib.import_module(f"day{day_num:02}")
    day_state = {}
    with timer("interpreting input"):
        parsed_input = apply_trim_args(day_module.parse, puzzle_input, day_state)
    with timer("running part 1"):
        part1 = apply_trim_args(day_module.part1, parsed_input, day_state)
    with timer("running part 2"):
        part2 = apply_trim_args(day_module.part2, parsed_input, day_state)
    print()
    print(f"part1:\n\n{part1}\n")
    print(f"part2:\n\n{part2}\n")


# general util functions:


def chunks_of(size, iterable):
    """
    Split into a list of lists of the given size.
    """
    args = [iter(iterable)] * size
    return [list(chunk) for chunk in zip(*args)]


def iter_chains(values):
    """
    Returns an iterator over the chains of repeated values in a sequence.
    """
    prev = values[0]
    chain = 1
    for value in values[1:]:
        if value == prev:
            chain = chain + 1
        else:
            yield prev, chain
            chain = 1
            prev = value
    yield prev, chain


def sign(number):
    """
    Return the sign of an integer (-1, 0, 1).
    """
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


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
