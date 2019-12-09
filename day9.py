"""
AdventOfCode2019 - Day 9
"""

import intcode

from day2 import parse


def part1(boost_program):
    """
    Solve for the answer to part 1.
    """
    outputs = []
    interpretor = intcode.Interpretor()
    interpretor.queue_input(1)
    while interpretor.run(boost_program):
        if interpretor.giving_output():
            outputs.append(interpretor.query_output())
    if len(outputs) > 1:
        print(f"WARNING: got {len(outputs) - 1} errors")
    return outputs[-1]


def part2(boost_program):
    """
    Solve for the answer to part 2.
    """
    outputs = []
    interpretor = intcode.Interpretor()
    interpretor.queue_input(2)
    while interpretor.run(boost_program):
        if interpretor.giving_output():
            outputs.append(interpretor.query_output())
    return outputs[-1]
