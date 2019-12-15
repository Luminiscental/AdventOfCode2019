"""General utility functions for all days."""
import functools
import math
import inspect
import time
import contextlib


@contextlib.contextmanager
def timer(desc):
    """Context manager for timing a block of code once and printing the time."""
    start = time.time()
    yield
    end = time.time()
    print(f"{desc}: took {end - start:0.5f} seconds")


def apply_trim_args(func, *args):
    """Apply a function to given arguments, using only as many as required."""
    arg_count = len(inspect.signature(func).parameters)
    return func(*args[:arg_count])


def chunks_of(size, iterable):
    """Split into a list of lists of the given size."""
    args = [iter(iterable)] * size
    return [list(chunk) for chunk in zip(*args)]


def iter_chains(values):
    """Returns an iterator over the chains of repeated values in a sequence."""
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
    """Return the sign of an integer (-1, 0, 1)."""
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def lcm(numbers):
    """Return the lowest common multiple of a sequence of numbers."""

    def lcm2(num1, num2):
        return num1 * num2 // math.gcd(num1, num2)

    return functools.reduce(lcm2, numbers)
