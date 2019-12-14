"""
AdventOfCode2019 - Day 2
"""

import intcode


def parse(puzzle_input):
    """
    Parse the input into a list of opcodes.
    """
    return [int(number) for number in puzzle_input.split(",")]


def run_prog(interpretor, program, noun, verb):
    """
    Run the program with a noun and verb and return the value at position 0.
    """
    edited = program.copy()
    edited[1] = noun
    edited[2] = verb
    # we don't expect any input requests so don't have to loop
    interpretor.run(edited)
    return interpretor.memory[0]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    return run_prog(intcode.Interpretor(), opcodes, 12, 2)


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    interpretor = intcode.Interpretor()

    # assume the program is linear
    constant_term = run_prog(interpretor, opcodes, 0, 0)
    noun_term = run_prog(interpretor, opcodes, 1, 0) - constant_term
    verb_term = run_prog(interpretor, opcodes, 0, 1) - constant_term

    assert verb_term == 1

    desired_output = 19690720
    verbs = [
        (desired_output - noun_term * noun - constant_term) // verb_term
        for noun in range(100)
    ]
    verbs = [verb for verb in verbs if verb >= 0]
    noun, verb = len(verbs) - 1, verbs[-1]

    assert run_prog(interpretor, opcodes, noun, verb) == desired_output

    return 100 * noun + verb
