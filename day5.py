"""
AdventOfCode2019 - Day 5
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
    outputs = []
    interpretor = intcode.Interpretor(lambda: 1, outputs.append)
    interpretor.run(opcodes)
    if any(output != 0 for output in outputs[:-1]):
        print(f"WARNING: test failed")
    return outputs[-1]


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    outputs = []
    interpretor = intcode.Interpretor(lambda: 5, outputs.append)
    interpretor.run(opcodes)
    return outputs[-1]
