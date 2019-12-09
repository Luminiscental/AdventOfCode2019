"""
AdventOfCode2019 - Day 7
"""

import itertools
import intcode

from day2 import parse


def pipeline(program, amplifiers, phase_settings, loop=False):
    """
    Run a signal that starts at 0 through a pipeline of amplifiers.
    """
    # setup phase settings
    for amplifier, phase_setting in zip(amplifiers, phase_settings):
        amplifier.queue_input(phase_setting)
    # run the signal through
    signal = 0
    curr = 0
    while curr < len(amplifiers) and amplifiers[curr].run(program):
        if amplifiers[curr].waiting_input():
            amplifiers[curr].receive_input(signal)
        elif amplifiers[curr].giving_output():
            signal = amplifiers[curr].query_output()
            curr += 1
            if loop:
                curr = curr % len(amplifiers)
    # we exit early (between output and halting) so reset manually
    for amplifier in amplifiers:
        amplifier.reset()
    return signal


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    amplifiers = [intcode.Interpretor() for _ in range(5)]
    return max(
        pipeline(opcodes, amplifiers, phase_settings)
        for phase_settings in itertools.permutations(range(5))
    )


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    amplifiers = [intcode.Interpretor() for _ in range(5)]
    return max(
        pipeline(opcodes, amplifiers, phase_settings, loop=True)
        for phase_settings in itertools.permutations(range(5, 10))
    )
