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

    contains_double = any(digits[i] == digits[i + 1] for i in range(len(digits) - 1))
    is_increasing = all(prev <= curr for prev, curr in zip(digits, digits[1:]))
    return contains_double and is_increasing


def part1(password_range):
    """
    Solve for the answer to part 1.
    """

    def pred(password):
        digits = [int(c) for c in str(password)]
        contains_double = any(prev == curr for prev, curr in zip(digits, digits[1:]))
        is_increasing = all(prev <= curr for prev, curr in zip(digits, digits[1:]))
        return contains_double and is_increasing

    return sum(1 for password in range(*password_range) if pred(password))


def part2(password_range):
    """
    Solve for the answer to part 2.
    """

    def pred(password):
        digits = [int(c) for c in str(password)]
        contains_double = False
        for i, _ in enumerate(digits):
            double_candidate = digits[i]
            double = digits[i : i + 2]
            surrounding = digits[max(0, i - 1) : i + 3]
            if (
                double.count(double_candidate) == 2
                and surrounding.count(double_candidate) == 2
            ):
                contains_double = True
        is_increasing = all(prev <= curr for prev, curr in zip(digits, digits[1:]))
        return contains_double and is_increasing

    return sum(1 for password in range(*password_range) if pred(password))
