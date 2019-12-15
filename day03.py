"""AdventOfCode2019 - Day 3"""


def build_wire(instructions):
    """Build a wire from a list of directions.
    Returns a dict from point to number of steps, excluding the origin.
    """
    wire = {}
    direction_map = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    total_steps = 0
    cursor_x, cursor_y = 0, 0
    for instr in instructions:
        direction = instr[0]
        steps = int(instr[1:])
        dir_x, dir_y = direction_map[direction]
        for step in range(1, steps + 1):
            cursor_x += dir_x
            cursor_y += dir_y
            # record the first time to get here only
            if (cursor_x, cursor_y) not in wire:
                wire[cursor_x, cursor_y] = total_steps + step
        total_steps += steps
    return wire


def parse(puzzle_input):
    """Parse the puzzle input."""
    return [build_wire(line.split(",")) for line in puzzle_input.splitlines()]


def part1(wires):
    """Solve for the answer to part 1."""
    intersections = set.intersection(*[set(wire.keys()) for wire in wires])
    return min(abs(point_x) + abs(point_y) for point_x, point_y in intersections)


def part2(wires):
    """Solve for the answer to part 2."""
    intersections = set.intersection(*[set(wire.keys()) for wire in wires])
    return min(
        sum(wire[point_x, point_y] for wire in wires)
        for point_x, point_y in intersections
    )
