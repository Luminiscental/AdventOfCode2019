"""
AdventOfCode2019 - Day 2
"""


def interpret(opcodes, noun, verb):
    """
    Run a list of opcodes.
    """
    memory = opcodes.copy()
    memory[1] = noun
    memory[2] = verb
    ipointer = 0

    def bin_op(op):
        lhs_ptr = memory[ipointer + 1]
        rhs_ptr = memory[ipointer + 2]
        out_ptr = memory[ipointer + 3]
        memory[out_ptr] = op(memory[lhs_ptr], memory[rhs_ptr])

    while True:
        opcode = memory[ipointer]
        if opcode == 1:
            bin_op(lambda a, b: a + b)
        elif opcode == 2:
            bin_op(lambda a, b: a * b)
        elif opcode == 99:
            break
        else:
            raise ValueError
        ipointer = ipointer + 4

    return memory[0]


def parse(puzzle_input):
    """
    Parse the input into a list of opcodes.
    """
    return [int(number) for number in puzzle_input.split(",")]


def part1(opcodes):
    """
    Solve for the answer to part 1.
    """
    return interpret(opcodes, 12, 2)


def part2(opcodes):
    """
    Solve for the answer to part 2.
    """

    def program(noun, verb):
        return interpret(opcodes, noun, verb)

    # assume program is linear
    constant_term = program(0, 0)
    noun_term = program(1, 0) - constant_term
    verb_term = program(0, 1) - constant_term

    desired_output = 19690720
    verbs = [
        (desired_output - noun_term * noun - constant_term) // verb_term
        for noun in range(100)
    ]
    verbs = [verb for verb in verbs if verb >= 0]
    noun, verb = len(verbs) - 1, verbs[-1]

    if program(noun, verb) != desired_output:
        print(f"WARNING: assumptions failed")

    return 100 * noun + verb
