"""AdventOfCode2019 - Day 21"""
import intcode
from util import ilast
from day02 import parse


class Droid:
    """Class to handle the springdroid."""

    def __init__(self, program, run=False):
        self.interpretor = intcode.Interpretor()
        self.program = program
        self.run = run

    def exec(self, script, debug=False):
        """Execute a script, given as a sequence of instructions."""
        for instr in script:
            self.interpretor.queue_inputs(map(ord, instr))
            self.interpretor.queue_input(ord("\n"))
        self.interpretor.queue_inputs(map(ord, "RUN\n" if self.run else "WALK\n"))
        if debug:
            for out in self.interpretor.run(self.program):
                print(out, end="")
        return ilast(self.interpretor.run(self.program))


def part1(program):
    """Solve for the answer to part 1."""
    script = [
        # J = not(A) or not(B) or not(C)
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        # J = D and (not(A) or not(B) or not(C))
        "NOT D T",
        "NOT T T",
        "AND T J",
    ]
    return Droid(program).exec(script)


def part2(program):
    """Solve for the answer to part 2."""
