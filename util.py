"""
General utility functions for all days.
"""

import sys
import time
import importlib
import contextlib
import requests
import inspect


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
