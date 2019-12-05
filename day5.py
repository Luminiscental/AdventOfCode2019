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

    def inputter():
        return 1

    def outputter(output):
        outputs.append(output)

    if any(output != 0 for output in outputs[:-1]):
        print(f"WARNING: test failed")

    interpretor = intcode.Interpretor(inputter, outputter)
    interpretor.run(opcodes)
    return outputs[-1]


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    return None
