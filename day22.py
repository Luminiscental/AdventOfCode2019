"""AdventOfCode2019 - Day 22

To simplify the problem consider the shuffle as a transformation on integers modulo deck size,
a transformation from position before the shuffle to position after. Each shuffling technique
is a simple operation:
    - Deal into a new stack: position -> -(position + 1)
    - Cut N cards:           position -> position - N
    - Deal with increment N: position -> N * position
By composing these we can combine the input into a single linear polynomial for the whole shuffle
sequence. Part 1 is simply evaluating this polynomial at a point. For part 2 we have to iterate
the polynomial, and then invert it at a point. Because the deck size is prime these operations
are not too painful.
"""
import re


def parse(puzzle_input):
    """Parse the puzzle input into the coefficients of the polynomial."""
    coeffs = [0, 1]  # start with the identity shuffle
    for line in puzzle_input.splitlines():
        if line.startswith("deal with"):
            number = int(re.search(r"\d+", line).group())
            # position -> number * position
            coeffs[0] *= number
            coeffs[1] *= number
        elif line.startswith("deal into"):
            # position -> -(position + 1)
            coeffs[0] += 1
            coeffs[0] *= -1
            coeffs[1] *= -1
        elif line.startswith("cut"):
            number = int(re.search(r"-?\d+", line).group())
            # position -> position - number
            coeffs[0] -= number
    return coeffs


def part1(coeffs):
    """Solve for the answer to part 1."""
    modulo = 10007
    # Evaluate the polynomial at 2019
    return (coeffs[0] + coeffs[1] * 2019) % modulo


def part2(coeffs):
    """Solve for the answer to part 2."""
    modulo = 119315717514047
    iterations = 101741582076661
    # Since modulo is prime inverting is exponentiation
    inv = lambda x: pow(x, modulo - 2, modulo)
    # Get the coefficients after iterating:
    # ax+b becomes a^n x + [(a^n - 1) / (a - 1)] b
    power = pow(coeffs[1], iterations, modulo)  # a^n
    coeffs[0] *= (power - 1) * inv(coeffs[1] - 1)
    coeffs[1] = power
    # Solve the equation:
    # ax + b = 2020 so x = (2020 - b) / a
    return (2020 - coeffs[0]) * inv(coeffs[1]) % modulo
