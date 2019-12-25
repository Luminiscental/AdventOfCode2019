"""AdventOfCode2019 - Day 25"""
import collections
import re
import intcode
from util import combinations
from day02 import parse

# Assuming the dangerous items are the same for everyone
DEATH_ITEMS = {
    "molten lava",
    "giant electromagnet",
    "infinite loop",
    "escape pod",
    "photons",
}

# Assuming the room layout is the same for everyone
TOUR = [
    "south",
    "west",
    "south",
    "north",
    "east",
    "north",
    "east",
    "west",
    "north",
    "east",
    "south",
    "south",
    "north",
    "north",
    "north",
    "north",
    "south",
    "south",
    "west",
    "north",
    "north",
    "west",
    "west",
    "east",
    "east",
    "north",
    "north",
    "north",
    "west",
]


def values_after(header, lines):
    """Get values after a header in a bullet list."""
    values = []
    if header in lines:
        start = lines.index(header) + 1
        for line in lines[start:]:
            if not line:
                break
            values.append(line[2:])  # skip the "- " characters
    return values


class Solver:
    """Simple AI to keep track of state and choose commands."""

    def __init__(self):
        self.password = None
        self.inv = []
        self.doors = list(reversed(TOUR))
        self.combinations = None
        self.combination = None

    def choose_command(self, description):
        """Returns which available command to use."""
        # Pick up all safe items
        items = values_after("Items here:", description.splitlines())
        for item in items:
            if item not in DEATH_ITEMS:
                self.inv.append(item)
                return f"take {item}"
        # Move along the tour to pick up everything
        if self.doors:
            return self.doors.pop()
        # At the end try every combination of items in increasing size order
        if self.combinations is None:
            self.combinations = list(combinations(self.inv, min_size=3))
        # Pick a new combination if needed
        if self.combination is None:
            self.combination = self.combinations.pop()
        # Drop all unneeded items
        for item in self.inv:
            if item not in self.combination:
                self.inv.remove(item)
                return f"drop {item}"
        # Pick up all needed items
        for item in self.combination:
            if item not in self.inv:
                self.inv.append(item)
                return f"take {item}"
        # Try to go south and signal that a new combination is needed
        self.combination = None
        return "south"


def part1(program):
    """Solve for the answer to part 1."""
    output_queue = []
    input_queue = collections.deque()
    solver = Solver()

    def ascii_input():
        nonlocal output_queue
        if not input_queue:
            description = bytes(output_queue).decode("ascii")
            output_queue = []
            command = solver.choose_command(description)
            input_queue.extend(bytes(command + "\n", "ascii"))
        return input_queue.popleft()

    interpretor = intcode.Interpretor(input_from=ascii_input)
    for code in interpretor.run(program):
        output_queue.append(code)
    finish_text = bytes(output_queue).decode("ascii")
    return int(re.search(r"\d+", finish_text).group(0))


def part2(_):
    """Solve for the answer to part 2."""
    return "Go click that button ;)"
