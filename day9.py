"""
AdventOfCode2019 - Day 9
"""

import intcode

from day2 import parse


def part1(boost_program):
    """
    Solve for the answer to part 1.
    """
    interpretor = intcode.Interpretor(collect_outputs=True)
    while interpretor.run(boost_program):
        if interpretor.state == intcode.RunState.WAITING_INPUT:
            interpretor.receive_input(1)
    if len(interpretor.outputs) > 1:
        print(f"WARNING: got {len(interpretor.outputs) - 1} errors")
    return interpretor.outputs[-1]


def part2(boost_program):
    """
    Solve for the answer to part 2.
    """
    interpretor = intcode.Interpretor(collect_outputs=True)
    while interpretor.run(boost_program):
        if interpretor.state == intcode.RunState.WAITING_INPUT:
            interpretor.receive_input(2)
    return interpretor.outputs[-1]
