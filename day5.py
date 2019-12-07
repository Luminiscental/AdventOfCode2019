"""
AdventOfCode2019 - Day 5
"""


import intcode


def parse(puzzle_input):
    """
    Parse the input into a list of opcodes.
    """
    return [int(number) for number in puzzle_input.split(",")]


def collect_outputs(program, input_constant):
    """
    Collect the outputs of a program, giving a constant value on any input call.
    """
    outputs = []
    interpretor = intcode.Interpretor()
    while interpretor.run(program):
        if interpretor.state == intcode.RunState.WAITING_INPUT:
            interpretor.receive_input(input_constant)
        elif interpretor.state == intcode.RunState.GIVING_OUTPUT:
            outputs.append(interpretor.query_output())
    return outputs


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    outputs = collect_outputs(opcodes, 1)
    if any(output != 0 for output in outputs[:-1]):
        print(f"WARNING: test failed")
    return outputs[-1]


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    return collect_outputs(opcodes, 5)[-1]
