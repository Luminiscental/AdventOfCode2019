"""
AdventOfCode2019 - Day 2
"""

import intcode


def parse(puzzle_input):
    """
    Parse the input into a list of opcodes.
    """
    return [int(number) for number in puzzle_input.split(",")]


def run_prog(program, noun, verb):
    """
    Run the program with a noun and verb and return the value at position 0.
    """
    edited = program.copy()
    edited[1] = noun
    edited[2] = verb
    interpretor = intcode.Interpretor()
    while interpretor.run(edited):
        pass  # expect no input/output
    return interpretor.memory[0]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    return run_prog(opcodes, 12, 2)


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """

    # assume run_prog is linear
    constant_term = run_prog(opcodes, 0, 0)
    noun_term = run_prog(opcodes, 1, 0) - constant_term
    verb_term = run_prog(opcodes, 0, 1) - constant_term

    desired_output = 19690720
    verbs = [
        (desired_output - noun_term * noun - constant_term) // verb_term
        for noun in range(100)
    ]
    verbs = [verb for verb in verbs if verb >= 0]
    noun, verb = len(verbs) - 1, verbs[-1]
    return 100 * noun + verb
