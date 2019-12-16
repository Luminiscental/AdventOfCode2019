"""AdventOfCode2019 - Day 16"""
import itertools
import multiprocessing
import functools
from util import repeat_each


def get_pattern(idx):
    """Get the coefficient pattern for a given index."""
    return itertools.cycle(repeat_each((1, 0, -1, 0), idx + 1))


def get_fft(signal, idx):
    """Get the digit after applying fft at a given index."""
    shifted_signal = signal[idx:]
    terms = zip(get_pattern(idx), shifted_signal)
    return abs(sum(coeff * number for coeff, number in terms)) % 10


def apply_fft(signal):
    """Apply the fft to an iterable signal."""
    calc_at_idx = functools.partial(get_fft, signal)
    with multiprocessing.Pool() as pool:
        return pool.map(calc_at_idx, range(len(signal)))


def display_signal(signal):
    """Return a string containing the digits of an iterable signal."""
    return "".join(str(number) for number in signal)


def parse(puzzle_input):
    """Parse the puzzle input into a list of numbers."""
    return [int(number) for number in puzzle_input.strip()]


def part1(signal):
    """Solve for the answer to part 1."""
    for _ in range(100):
        signal = apply_fft(signal)
    return display_signal(signal[:8])


def part2(signal):
    """Solve for the answer to part 2."""

    message_offset = int(display_signal(signal[:7]))
    signal = signal * 10000

    # in the latter half of the signal the pattern is just 0,...,0,1,...,1.
    # in the last row there is 1 one, the second from last has 2 ones, e.t.c.
    # repeatedly applying this pattern gives diagonals from Pascal's triangle as coefficients.

    # weights[i] = (99 + i) choose (99)
    # this is an iterative way to calculate all the binomial coefficients we'll need
    # it's more efficient than calling a general choose function
    weights = [1]
    for i in range(len(signal) - message_offset):
        weights.append(weights[-1] * (100 + i) // (1 + i))

    def get_output_at(idx):
        assert idx > len(signal) / 2, "message offset was too early for this method"
        from_back = len(signal) - idx
        return sum(weights[i] * signal[i - from_back] for i in range(from_back)) % 10

    return display_signal(map(get_output_at, range(message_offset, message_offset + 8)))
