"""AdventOfCode2019 - Day 11"""
import intcode
from day02 import parse

WHITE, BLACK = RIGHT, LEFT = 1, 0


class Robot:
    """A class representing the panel painting robot."""

    def __init__(self, program):
        self.program = program
        self.interpretor = intcode.Interpretor()
        self.panels = set()  # the set of white panels
        self.painted = set()  # the set of panels that were ever painted
        self.position = 0, 0
        self.facing = 0, -1  # up is negative

    def paint(self, color):
        """Paint the current panel white or black."""
        if color == WHITE:
            self.panels.add(self.position)
            self.painted.add(self.position)
        else:
            self.panels.discard(self.position)

    def check(self):
        """Check the color of the current panel."""
        return WHITE if self.position in self.panels else BLACK

    def turn(self, direction):
        """Turn in a direction and step forward."""
        # up is negative
        if direction == RIGHT:
            self.facing = -self.facing[1], self.facing[0]
        else:
            self.facing = self.facing[1], -self.facing[0]
        self.position = (
            self.position[0] + self.facing[0],
            self.position[1] + self.facing[1],
        )

    def run(self):
        """Run the painting program."""
        while self.interpretor.run(self.program):
            if self.interpretor.waiting_input():
                self.interpretor.receive_input(self.check())
            for color, direction in self.interpretor.output(group_size=2):
                self.paint(color)
                self.turn(direction)

    def display_panels(self):
        """Return a string representation of the painted panels."""
        minx = min(x for x, y in self.panels)
        maxx = max(x for x, y in self.panels)
        miny = min(y for x, y in self.panels)
        maxy = max(y for x, y in self.panels)
        return "\n".join(
            "".join(
                "█" if (panel_x, panel_y) in self.panels else " "
                for panel_x in range(minx, maxx + 1)
            )
            for panel_y in range(miny, maxy + 1)
        )


def part1(program):
    """Solve for the answer to part 1."""
    robot = Robot(program)
    robot.run()
    return len(robot.painted)


def part2(program):
    """Solve for the answer to part 2."""
    robot = Robot(program)
    robot.paint(WHITE)  # start on white this time
    robot.run()
    return robot.display_panels()
