"""General utility functions for all days."""
import functools
import math
import inspect
import time
import contextlib
import itertools


def replace_occurences(sequence, subsequence, replacement):
    """Replace occurences of a subsequence in a sequence."""
    while True:
        for i in range(len(sequence)):
            if sequence[i : i + len(subsequence)] == subsequence:
                sequence[i : i + len(subsequence)] = replacement
                break
        else:
            break


def count_occurences(sequence, subsequence):
    """Count occurences of a subsequence in a sequence."""
    return ilen(
        i
        for i in range(len(sequence))
        if sequence[i : i + len(subsequence)] == subsequence
    )


def ilen(iterable):
    """Count the length of an iterable."""
    return sum(1 for _ in iterable)


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


def repeat_each(iterable, count):
    """Make an iterator repeating every element of an iterable a given number of times."""
    for elem in iterable:
        for _ in range(count):
            yield elem


def chunks_of(size, iterable):
    """Split an iterable into a list of lists of the given size."""
    args = [iter(iterable)] * size
    return [list(chunk) for chunk in zip(*args)]


def chain_lengths(values):
    """Returns a generator of the lengths of chains of repeated values in a sequence."""
    return (ilen(group) for _, group in itertools.groupby(values))


def sign(number):
    """Return the sign of an integer (-1, 0, 1)."""
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def lcm(num1, num2):
    """Return the lowest common multiple of a pair of integers."""
    return num1 * num2 // math.gcd(num1, num2)


def lcm_all(numbers):
    """Return the lowest common multiple of a sequence of integers."""
    return functools.reduce(lcm, numbers)
