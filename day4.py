"""
AdventOfCode2019 - Day 4
"""


def parse(puzzle_input):
    """
    Parse the password range from the input.
    """
    elems = [int(elem) for elem in puzzle_input.split("-")]
    return elems[0], elems[1]


def password_predicate(password):
    """
    Check if a given password number meet the criteria.
    """
    digits = [int(c) for c in str(password)]
    contains_repeat = any(digits[i] == digits[i + 1] for i in range(len(digits) - 1))
    is_increasing = all(prev <= curr for prev, curr in zip(digits, digits[1:]))
    return contains_repeat and is_increasing


def part1(password_range):
    """
    Solve for the answer to part 1.
    """
    return sum(1 for password in range(*password_range) if password_predicate(password))


def part2(password_range):
    """
    Solve for the answer to part 1.
    """
