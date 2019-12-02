"""
AdventOfCode2019 - Day 2
"""

import util

PUZZLE_INPUT = [int(number) for number in util.get_input(2).split(",")]


class UnknownOpcodeException(Exception):
    """
    Exception class for an unknown opcode given to an Intcode interpretor.
    """


class Interpretor:
    """
    An Intcode interpretor.
    """

    def __init__(self):
        self.memory = []

    def bin_op(self, index, func):
        """
        Perform a binary operation reading locations from the index.
        """
        lhs_read = self.memory[index + 1]
        rhs_read = self.memory[index + 2]
        out = self.memory[index + 3]
        self.memory[out] = func(self.memory[lhs_read], self.memory[rhs_read])

    def run(self, opcodes, noun, verb):
        """
        Run a list of opcodes.
        """
        self.memory = opcodes.copy()
        self.memory[1] = noun
        self.memory[2] = verb

        ipointer = 0
        while True:
            opcode = self.memory[ipointer]
            if opcode == 1:
                self.bin_op(ipointer, lambda a, b: a + b)
            elif opcode == 2:
                self.bin_op(ipointer, lambda a, b: a * b)
            elif opcode == 99:
                break
            else:
                raise UnknownOpcodeException
            ipointer = ipointer + 4

        return self.memory[0]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    interpretor = Interpretor()
    return interpretor.run(opcodes, 12, 2)


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """
    interpretor = Interpretor()

    def program(noun, verb):
        return interpretor.run(opcodes, noun, verb)

    # assume program is linear
    constant_term = program(0, 0)
    noun_term = program(1, 0) - constant_term
    verb_term = program(0, 1) - constant_term

    if verb_term != 1:
        print("WARNING: verb coefficient is non-unit")

    def program_native(noun, verb):
        return constant_term + noun_term * noun + verb_term * verb

    for noun, verb in zip(range(0, 5), range(0, 5)):
        if program(noun, verb) != program_native(noun, verb):
            print("WARNING: program is not linear")

    desired_output = 19690720
    verbs = [(desired_output - noun_term * noun - constant_term) //
             verb_term for noun in range(100)]
    verbs = [verb for verb in verbs if verb >= 0]
    noun, verb = len(verbs) - 1, verbs[-1]
    if program(noun, verb) != desired_output:
        print(f"WARNING: minimal solution failed")
    return 100 * noun + verb


if __name__ == "__main__":
    print(f"part1: {part1(PUZZLE_INPUT)}")
    print(f"part2: {part2(PUZZLE_INPUT)}")
