"""AdventOfCode2019 - Day 25"""
from typing import Callable, Sequence, Optional
import collections
import re
import dataclasses
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


@dataclasses.dataclass
class Action:
    """Class representing a queued action."""

    command: Optional[str] = None
    preaction: Optional[Callable[[str], None]] = None
    inventory: Optional[Sequence[str]] = None


class Solver:
    """Simple AI to keep track of state and choose commands."""

    def __init__(self):
        self.password = None
        self.inv = []
        self.queue = collections.deque()
        self.tour = list(reversed(TOUR))
        self.light_items = set()

    def queue_command(self, command, inventory=None):
        """Queue a single command to execute."""
        if self.queue and self.queue[-1].command is None:
            self.queue[-1].command = command
            self.queue[-1].inventory = inventory
        else:
            self.queue.append(Action(command=command, inventory=inventory))

    def queue_commands(self, commands):
        """Queue an iterable of commands to execute."""
        for command in commands:
            self.queue_command(command)

    def get_command(self, description):
        """Get the next command to execute given the current description."""
        if not self.queue:
            self.choose_action(description)
        action = self.queue.popleft()
        if action.preaction is not None:
            # Perform any preaction
            action.preaction(description)
            action.preaction = None
        if action.inventory is not None:
            # Drop all unneeded items
            for item in self.inv:
                if item not in action.inventory:
                    self.queue.appendleft(action)
                    self.inv.remove(item)
                    return f"drop {item}"
            # Pick up all needed items
            for item in action.inventory:
                if item not in self.inv:
                    self.queue.appendleft(action)
                    self.inv.append(item)
                    return f"take {item}"
        if action.command is None:  # if there was only a hook try another command
            return self.get_command(description)
        return action.command

    def then(self, func):
        """Add a hook to the next command."""
        self.queue.append(Action(preaction=func))

    def choose_action(self, description):
        """Queue commands to execute given the current description."""
        lines = description.splitlines()
        # If there are safe items to pick up pick them up
        safe_items = {
            item
            for item in values_after("Items here:", lines)
            if item not in DEATH_ITEMS
        }
        if safe_items:
            self.queue_commands(f"take {item}" for item in safe_items)
            self.inv.extend(safe_items)
            return
        # If we haven't finished the tour keep going
        if self.tour:
            self.queue_command(self.tour.pop())
            return
        # If we've reached the end figure out what items are light
        if not self.light_items:
            for item in self.inv:
                self.queue_command("south", inventory=[item])

                def check_was_light(description, item=item):
                    if "heavier" in description:
                        self.light_items.add(item)

                self.then(check_was_light)
            return
        # Try all big enough combinations of light items in decreasing size order
        inventories = combinations(self.light_items, min_size=2)
        for inv in sorted(inventories, key=len, reverse=True):
            self.queue_command("south", inv)


def part1(program):
    """Solve for the answer to part 1."""
    output_queue = []
    solver = Solver()
    interpretor = intcode.Interpretor()

    def ascii_input():
        description = bytes(output_queue).decode("ascii")
        output_queue.clear()
        command = solver.get_command(description)
        inputs = bytes(command + "\n", "ascii")
        interpretor.queue_inputs(inputs[1:])
        return inputs[0]

    interpretor.input_from = ascii_input
    for code in interpretor.run(program):
        output_queue.append(code)
    finish_text = bytes(output_queue).decode("ascii")
    return int(re.search(r"\d+", finish_text).group(0))


def part2(_):
    """Solve for the answer to part 2."""
    return "Go click that button ;)"
