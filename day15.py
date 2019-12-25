"""AdventOfCode2019 - Day 15"""
import intcode
from util import bfs, tuple_add
from day02 import parse

NORTH, EAST, SOUTH, WEST = tuple(range(4))
HIT_WALL, MOVED, FOUND_STATION = 0, 1, 2
DIRECTION_TO_OFFSET = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0), EAST: (1, 0)}
DIRECTION_TO_INPUT = {NORTH: 1, SOUTH: 2, WEST: 3, EAST: 4}


class Robot:
    """Class wrapping the remote robot state."""

    def __init__(self, program):
        self.interpretor = intcode.Interpretor()
        self.program_output = self.interpretor.run(program)

        self.pos = 0, 0
        self.station = None
        self.maze = {}

    def calc_move(self, direction):
        """Calculate the resulting position of moving in a direction."""
        return tuple_add(self.pos, DIRECTION_TO_OFFSET[direction])

    def update_state(self, output, move):
        """Update based on an output code. Returns whether the move was successful."""
        target = self.calc_move(move)
        self.maze[target] = output
        if output == FOUND_STATION:
            self.station = target
        if output != HIT_WALL:
            self.pos = target
            return True
        return False

    def move(self, direction, reverse=False):
        """Move in a direction. Returns whether the move was successful."""
        if reverse:
            direction = (direction + 2) % 4
        self.interpretor.queue_input(DIRECTION_TO_INPUT[direction])
        return self.update_state(next(self.program_output), direction)

    def explore(self):
        """Explore the maze until no new squares can be found using DFS."""
        for direction in range(4):
            if self.calc_move(direction) not in self.maze and self.move(direction):
                self.explore()
                self.move(direction, reverse=True)


def part1(program, state):
    """Solve for the answer to part 1."""
    robot = Robot(program)
    robot.explore()
    station = state["station"] = robot.station
    maze = state["maze"] = robot.maze
    distance, _ = bfs(
        traversable_pred=lambda pos: maze[pos] != HIT_WALL,
        start_node=(0, 0),
        end_node=station,
    )
    return distance


def part2(_, state):
    """Solve for the answer to part 2."""
    maze = state["maze"]
    station = state["station"]
    return bfs(
        traversable_pred=lambda pos: maze[pos] != HIT_WALL,
        start_node=station,
        initial_state=-1,
        state_updater=lambda pos, dist, curr_max: max(dist, curr_max),
    )
