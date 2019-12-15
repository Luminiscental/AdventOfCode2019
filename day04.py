"""AdventOfCode2019 - Day 4"""
from util import iter_chains


def parse(puzzle_input):
    """Parse the puzzle input into a list of increasing digit passwords in the range."""
    start, end = [int(number) for number in puzzle_input.split("-")]
    passwords = [str(number) for number in range(start, end)]
    return [password for password in passwords if sorted(password) == list(password)]


def part1(passwords):
    """Solve for the answer to part 1."""
    return sum(
        1
        for password in passwords
        if any(chain_length >= 2 for _, chain_length in iter_chains(password))
    )


def part2(passwords):
    """Solve for the answer to part 2."""
    return sum(
        1
        for password in passwords
        if any(chain_length == 2 for _, chain_length in iter_chains(password))
    )
