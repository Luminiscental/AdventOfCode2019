"""
AdventOfCode2019 - Day 5
"""


import intcode

from day02 import parse


def run_tests(program, input_constant):
    """
    Run the tests giving a certain input.
    """
    interpretor = intcode.Interpretor()
    interpretor.queue_input(input_constant)
    # we don't expect any more input requests so don't have to loop
    interpretor.run(program)
    outputs = list(interpretor.output_queue)
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
