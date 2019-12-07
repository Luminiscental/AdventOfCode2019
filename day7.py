"""
AdventOfCode2019 - Day 7
"""

import itertools
import intcode


class Amplifier:
    """
    An amplifier in the sequence.
    """

    def __init__(self, program, prev=None):
        self.prev = prev
        self.output = None
        self.input = []

        self.interpretor = intcode.Interpretor(self.get_input, self.put_output)
        self.program = program

    def get_input(self):
        """
        Get the input to give to the program.
        """
        return self.input.pop()

    def put_output(self, output):
        """
        Store the output value calculated by the program.
        """
        self.output = output

    def run(self, phase_setting):
        """
        Calculate the output value given a phase setting.
        """
        prev_output = 0 if self.prev is None else self.prev.output
        self.input = [prev_output, phase_setting]
        self.interpretor.run(self.program)


def create_amp_sequence(program, count):
    """
    Make a linked sequence of amplifiers, returned in a list.
    """
    result = []
    for _ in range(count):
        result.append(Amplifier(program, prev=result[-1] if result else None))
    return result


def parse(puzzle_input):
    """
    Parse the puzzle input into a list of opcodes.
    """
    return [int(number) for number in puzzle_input.split(",")]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    amplifiers = create_amp_sequence(opcodes, 5)

    def calc_output(settings):
        for setting, amplifier in zip(settings, amplifiers):
            amplifier.run(setting)
        return amplifiers[-1].output

    return max(map(calc_output, itertools.permutations(range(5))))


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
