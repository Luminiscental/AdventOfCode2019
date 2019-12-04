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


def increasing(sequences):
    """
    Given a sequence of sequences return a list over all the sequences that are increasing.
    """
    return [
        sequence
        for sequence in sequences
        if all(prev <= curr for prev, curr in zip(sequence, sequence[1:]))
    ]


def parse(puzzle_input):
    """
    Parse the puzzle input into a list of increasing digit lists in the range.
    """
    return increasing(
        [int(c) for c in str(password)]
        for password in range(*[int(number) for number in puzzle_input.split("-")])
    )


def part1(passwords):
    """
    Solve for the answer to part 1.
    """
    return sum(
        1
        for password in passwords
        if any(chain_length >= 2 for _, chain_length in iter_chains(password))
    )


def part2(passwords):
    """
    Solve for the answer to part 2.
    """
    return sum(
        1
        for password in passwords
        if any(chain_length == 2 for _, chain_length in iter_chains(password))
    )
