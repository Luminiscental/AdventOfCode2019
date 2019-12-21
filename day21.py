"""AdventOfCode2019 - Day 21"""
import intcode
from util import ilast
from day02 import parse


class Droid:
    """Class to handle the springdroid."""

    def __init__(self, program):
        self.interpretor = intcode.Interpretor()
        self.program = program

    def exec(self, script, run=False, debug=False):
        """Execute a script, given as a sequence of instructions."""
        for instr in script:
            self.interpretor.queue_inputs(map(ord, instr))
            self.interpretor.queue_input(ord("\n"))
        self.interpretor.queue_inputs(map(ord, "RUN\n" if run else "WALK\n"))
        if debug:
            for out in self.interpretor.run(self.program):
                print(chr(out), end="")
        return ilast(self.interpretor.run(self.program))


def part1(program):
    """Solve for the answer to part 1."""
    script = [
        "NOT A J",  # J=~A
        "NOT B T",  # T=~B
        "OR T J",  # J=~A|~B
        "NOT C T",  # T=~C
        "OR T J",  # J=~A|~B|~C
        "NOT D T",  # T=~D
        "NOT T T",  # T=D
        "AND T J",  # J=D&(~A|~B|~C)
    ]
    return Droid(program).exec(script)


def part2(program):
    """Solve for the answer to part 2."""
    script = [
        "NOT A J",  # J=~A
        "NOT B T",  # T=~B
        "OR T J",  # J=~A|~B
        "NOT C T",  # T=~C
        "OR T J",  # J=~A|~B|~C
        "NOT D T",  # T=~D
        "NOT T T",  # T=D
        "AND T J",  # J=D&(~A|~B|~C)
        "NOT E T",  # T=~E
        "NOT T T",  # T=E
        "OR H T",  # T=H|E
        "AND T J",  # J=D&(H|E)&(~A|~B|~C)
    ]
    return Droid(program).exec(script, run=True)
