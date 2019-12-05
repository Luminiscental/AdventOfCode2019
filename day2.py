"""
AdventOfCode2019 - Day 2
"""

import intcode


def parse(puzzle_input):
    """
    Parse the input into a list of opcodes.
    """
    return [int(number) for number in puzzle_input.split(",")]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    edited = opcodes.copy()
    edited[1] = 12
    edited[2] = 2
    return intcode.Interpretor().run(edited)


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """

    def program(noun, verb):
        edited = opcodes.copy()
        edited[1] = noun
        edited[2] = verb
        return intcode.Interpretor().run(edited)

    # assume program is linear
    constant_term = program(0, 0)
    noun_term = program(1, 0) - constant_term
    verb_term = program(0, 1) - constant_term

    desired_output = 19690720
    verbs = [
        (desired_output - noun_term * noun - constant_term) // verb_term
        for noun in range(100)
    ]
    verbs = [verb for verb in verbs if verb >= 0]
    noun, verb = len(verbs) - 1, verbs[-1]

    if program(noun, verb) != desired_output:
        print(f"WARNING: assumptions failed")

    return 100 * noun + verb
