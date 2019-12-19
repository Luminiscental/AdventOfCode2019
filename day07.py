"""AdventOfCode2019 - Day 7"""
import collections
import itertools
import intcode
from day02 import parse

Amplifier = collections.namedtuple("Amplifier", "interpretor output")


def pipeline(program, amplifier_count, phase_settings, loop=False):
    """Run a signal that starts at 0 through a pipeline of amplifiers."""
    # Create the amplifiers
    amplifiers = [
        Amplifier(interpretor, output=interpretor.run(program))
        for _ in range(amplifier_count)
        for interpretor in [intcode.Interpretor()]
    ]
    # Setup phase settings
    for amplifier, phase_setting in zip(amplifiers, phase_settings):
        amplifier.interpretor.queue_input(phase_setting)
    # Run the signal through
    signal = 0
    curr = 0
    while curr < len(amplifiers):
        amplifiers[curr].interpretor.queue_input(signal)
        try:
            signal = next(amplifiers[curr].output)
        except StopIteration:
            break
        curr += 1
        if loop:
            curr = curr % len(amplifiers)
    return signal


def part1(opcodes):
    """Solve for the answer to part 1."""
    return max(
        pipeline(opcodes, 5, phase_settings)
        for phase_settings in itertools.permutations(range(5))
    )


def part2(opcodes):
    """Solve for the answer to part 2."""
    return max(
        pipeline(opcodes, 5, phase_settings, loop=True)
        for phase_settings in itertools.permutations(range(5, 10))
    )
