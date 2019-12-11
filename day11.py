"""
AdventOfCode2019 - Day 11
"""

import intcode

from day02 import parse

WHITE = 1
BLACK = 0

RIGHT = 1
LEFT = 0


class Robot:
    """
    A class representing the panel painting robot.
    """

    def __init__(self, program):
        self.program = program
        self.interpretor = intcode.Interpretor()
        self.panels = set()  # the set of white panels
        self.position = 0, 0
        self.facing = 0, -1  # up is negative

        self.painted = set()

    def paint(self, color):
        """
        Paint the current panel white or black.
        """
        if color == WHITE:
            self.panels.add(self.position)
            self.painted.add(self.position)
        else:
            self.panels.discard(self.position)

    def check(self):
        """
        Check the color of the current panel.
        """
        return WHITE if self.position in self.panels else BLACK

    def turn(self, direction):
        """
        Turn in a direction and step forward.
        """
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
        """
        Run the program.
        """
        output_queue = []
        while self.interpretor.run(self.program):
            if self.interpretor.waiting_input():
                self.interpretor.receive_input(self.check())
            if self.interpretor.giving_output():
                output_queue.append(self.interpretor.query_output())
                if len(output_queue) == 2:
                    color = output_queue.pop(0)
                    direction = output_queue.pop(0)
                    self.paint(color)
                    self.turn(direction)


def part1(program, state):
    """
    Solve for the answer to part 1.
    """
    robot = Robot(program)
    state["robot"] = robot
    robot.run()
    return len(robot.painted)


def part2(program, state):
    """
    Solve for the answer to part 2.
    """
    robot = state["robot"]
