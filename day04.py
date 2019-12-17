"""AdventOfCode2019 - Day 4"""
from util import chain_lengths, ilen


def parse(puzzle_input):
    """Parse the puzzle input into a list of increasing digit passwords in the range."""
    start, end = [int(number) for number in puzzle_input.split("-")]
    passwords = [str(number) for number in range(start, end)]
    return [password for password in passwords if sorted(password) == list(password)]


def part1(passwords):
    """Solve for the answer to part 1."""

    def valid(password):
        return any(chain >= 2 for chain in chain_lengths(password))

    return ilen(filter(valid, passwords))


def part2(passwords):
    """Solve for the answer to part 2."""

    def valid(password):
        return any(chain == 2 for chain in chain_lengths(password))

    return ilen(filter(valid, passwords))
