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
    Collect the outputs of a program, giving a constant value on the first input call.
    """
    outputs = []
    interpretor = intcode.Interpretor()
    interpretor.queue_input(input_constant)
    while interpretor.run(program):
        if interpretor.state == intcode.RunState.GIVING_OUTPUT:
            outputs.append(interpretor.query_output())
    return outputs


def run_tests(program, input_constant):
    """
    Run the tests giving a certain input.
    """
    outputs = collect_outputs(program, input_constant)
    if any(output != 0 for output in outputs[:-1]):
        print(f"WARNING: test failed")
    return outputs[-1]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    return run_tests(opcodes, input_constant=1)


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    return run_tests(opcodes, input_constant=5)
