"""AdventOfCode2019 - Day 7"""
import itertools
import intcode
from day02 import parse


def pipeline(program, amplifiers, phase_settings, loop=False):
    """Run a signal that starts at 0 through a pipeline of amplifiers."""
    # setup phase settings
    for amplifier, phase_setting in zip(amplifiers, phase_settings):
        amplifier.queue_input(phase_setting)
    # run the signal through
    signal = 0
    curr = 0
    while curr < len(amplifiers) and amplifiers[curr].run(program):
        if amplifiers[curr].waiting_input():
            amplifiers[curr].receive_input(signal)
        for curr_output in amplifiers[curr].output():
            signal = curr_output
            curr += 1
            if loop:
                curr = curr % len(amplifiers)
    # we exit early (between output and halting) so reset manually
    for amplifier in amplifiers:
        amplifier.reset()
    return signal


def part1(opcodes, state):
    """Solve for the answer to part 1."""
    state["amplifiers"] = [intcode.Interpretor() for _ in range(5)]
    return max(
        pipeline(opcodes, state["amplifiers"], phase_settings)
        for phase_settings in itertools.permutations(range(5))
    )


def part2(opcodes, state):
    """Solve for the answer to part 2."""
    return max(
        pipeline(opcodes, state["amplifiers"], phase_settings, loop=True)
        for phase_settings in itertools.permutations(range(5, 10))
    )
