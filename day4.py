"""
AdventOfCode2019 - Day 4
"""


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


def parse(puzzle_input):
    """
    Parse the puzzle input into a list of digit lists.
    """
    return [
        [int(c) for c in str(password)]
        for password in range(*[int(number) for number in puzzle_input.split("-")])
    ]


def part1(passwords):
    """
    Solve for the answer to part 1.
    """

    def pred(digits):
        contains_double = any(
            chain_length >= 2 for _, chain_length in iter_chains(digits)
        )
        is_increasing = all(prev <= curr for prev, curr in zip(digits, digits[1:]))
        return contains_double and is_increasing

    return sum(1 for password in passwords if pred(password))


def part2(passwords):
    """
    Solve for the answer to part 2.
    """

    def pred(digits):
        contains_double = any(
            chain_length == 2 for _, chain_length in iter_chains(digits)
        )
        is_increasing = all(prev <= curr for prev, curr in zip(digits, digits[1:]))
        return contains_double and is_increasing

    return sum(1 for password in passwords if pred(password))
