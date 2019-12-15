"""AdventOfCode2019 - Day 15"""
import collections
import operator
import intcode
from day02 import parse

NORTH, EAST, SOUTH, WEST = tuple(range(4))
HIT_WALL, MOVED, FOUND_STATION = 0, 1, 2
DIRECTION_TO_OFFSET = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0), EAST: (1, 0)}
DIRECTION_TO_INPUT = {NORTH: 1, SOUTH: 2, WEST: 3, EAST: 4}


class Robot:
    """Class wrapping the remote robot state."""

    def __init__(self, program):
        self.interpretor = intcode.Interpretor()
        self.program = program

        self.pos = 0, 0
        self.station = None
        self.maze = {}

    def calc_move(self, direction):
        """Calculate the resulting position of moving in a direction."""
        return tuple(map(operator.add, self.pos, DIRECTION_TO_OFFSET[direction]))

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
        while self.interpretor.run(self.program):
            for output in self.interpretor.output():
                return self.update_state(output, direction)

    def explore(self):
        """Explore the maze until no new squares can be found using DFS."""
        for direction in range(4):
            if self.calc_move(direction) not in self.maze and self.move(direction):
                self.explore()
                self.move(direction, reverse=True)


def bfs(obstructed, *, start=(0, 0), target=None):
    """Find the distance to a target, or until the maze is filled, using BFS."""
    if (start in obstructed) or (target is not None and target in obstructed):
        raise ValueError("No path exists")
    Node = collections.namedtuple("Node", "pos dist")
    visited = set()
    max_dist = -1
    queue = collections.deque()

    queue.append(Node(pos=start, dist=0))
    visited.add(start)
    while queue:
        curr = queue.pop()
        if curr.pos == target:
            return curr.dist
        if curr.dist > max_dist:
            max_dist = curr.dist
        for offset in DIRECTION_TO_OFFSET.values():
            adjacent = tuple(map(operator.add, curr.pos, offset))
            if adjacent not in visited | obstructed:
                queue.append(Node(pos=adjacent, dist=curr.dist + 1))
                visited.add(adjacent)

    if target is not None:
        raise ValueError("No path to target found")
    return max_dist


def part1(program, state):
    """Solve for the answer to part 1."""
    robot = Robot(program)
    robot.explore()
    state["walls"] = {tile for tile in robot.maze if robot.maze[tile] == HIT_WALL}
    state["station"] = robot.station
    return bfs(state["walls"], target=state["station"])


def part2(_, state):
    """Solve for the answer to part 2."""
    return bfs(state["walls"], start=state["station"])
