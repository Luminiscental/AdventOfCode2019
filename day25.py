"""AdventOfCode2019 - Day 25

Some pretty ugly / complex code to do BFS and item combination testing.
As far as I know this should work for any person's input.
"""
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

BACKTRACK = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


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


class Explorer:
    """Simple AI to explore the layout of the game using DFS."""

    def __init__(self, parent):
        self.inv = parent.inv
        self.route = None
        self.exit = None
        self.path = tuple()
        self.seen_paths = set()
        self.seen_rooms = set()

    def get_commands(self, description):
        """Yield commands to execute given the current description."""
        lines = description.splitlines()
        items = values_after("Items here:", lines)
        doors = values_after("Doors here lead:", lines)
        # Pick up any safe items
        for item in items:
            if item not in DEATH_ITEMS:
                self.inv.add(item)
                yield f"take {item}"
        # Check if we found the exit room
        if "next room" in description:
            if self.route is None:
                self.route = self.path
                for door in doors:
                    if door != BACKTRACK[self.path[-1]]:
                        self.exit = door
                        break
        else:
            for door in doors:
                if self.path and door == BACKTRACK[self.path[-1]]:
                    continue
                if self.path + (door,) in self.seen_paths:
                    continue
                self.path += (door,)
                self.seen_paths.add(self.path)
                yield door
                return
        # Backtrack if we can't move forward
        if self.path:
            self.path, last = self.path[:-1], self.path[-1]
            yield BACKTRACK[last]


class Solver:
    """Simple AI to solve the text adventure game."""

    def __init__(self):
        self.inv = set()
        self.explorer = Explorer(self)
        self.at_end = False
        self.command_queue = collections.deque()
        self.light_items = set()

    def queue_command(self, command, inventory=None):
        """Queue a command for execution."""
        self.command_queue.append((command, inventory))

    def queue_commands(self, commands):
        """Queue an iterable of commands for execution."""
        for command in commands:
            self.queue_command(command)

    def get_command(self, description):
        """Return a command to execute given the current description."""
        # Return any queued commands
        if self.command_queue:
            command, inventory = self.command_queue.popleft()
            if inventory is not None:
                for item in inventory:
                    if item not in self.inv:
                        self.command_queue.appendleft((command, inventory))
                        self.inv.add(item)
                        return f"take {item}"
                for item in self.inv:
                    if item not in inventory:
                        self.command_queue.appendleft((command, inventory))
                        self.inv.remove(item)
                        return f"drop {item}"
            if isinstance(command, str):
                return command
            command(description)
            return self.get_command(description)
        # Get to the penultimate room
        if not self.at_end:
            explore_commands = list(self.explorer.get_commands(description))
            if explore_commands:
                self.queue_commands(explore_commands)
                return self.get_command(description)
            assert self.explorer.route is not None, "Could not find the exit"
            self.queue_commands(self.explorer.route)
            self.at_end = True
            return self.get_command(description)
        # Figure out which items are light
        if not self.light_items:
            for item in self.inv:
                self.queue_command(self.explorer.exit, inventory=[item])

                def check_was_light(description, item=item):
                    if "heavier" in description:
                        self.light_items.add(item)

                self.queue_command(check_was_light)
            return self.get_command(description)
        # Try all big enough combinations of light items
        for combination in sorted(
            combinations(self.light_items, min_size=2), key=len, reverse=True
        ):
            self.queue_command(self.explorer.exit, inventory=combination)
        return self.get_command(description)


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
