"""AdventOfCode2019 - Day 21"""
import intcode
from util import ilast
from day02 import parse


def run_droid(program, script, walk=True, debug=False):
    """Execute a springdroid script, expected as a sequence of instruction strings."""
    interpretor = intcode.Interpretor()
    for instr in script:
        interpretor.queue_inputs(map(ord, instr))
        interpretor.queue_input(ord("\n"))
    interpretor.queue_inputs(map(ord, "WALK\n" if walk else "RUN\n"))
    if debug:
        for out in interpretor.run(program):
            print(chr(out), end="")
    return ilast(interpretor.run(program))


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
    return run_droid(program, script)


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
    return run_droid(program, script, walk=False)
