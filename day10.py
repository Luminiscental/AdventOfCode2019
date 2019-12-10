"""
AdventOfCode2019 - Day 10
"""
from collections import namedtuple
import math

AsteroidField = namedtuple("AsteroidField", "width height asteroids")


def get_directions(width, height, order_cw=False):
    """
    Get a list of the x and y steps for every direction within the region.
    """
    result = [
        (x_step, y_step)
        for x_step in range(1 - width, width)
        if x_step < width
        for y_step in range(1 - height, height)
        if y_step < height
        and (x_step, y_step) != (0, 0)
        and math.gcd(x_step, y_step) == 1
    ]
    if order_cw:
        result.sort(key=lambda direction: math.atan2(direction[1], direction[0]))
    return result


def raycast(field, location, direction):
    """
    Return the position of the first asteroid hit, or None.
    """
    x_step, y_step = direction
    loc_x, loc_y = location
    look_x, look_y = loc_x + x_step, loc_y + y_step
    while 0 <= look_x < field.width and 0 <= look_y < field.height:
        if (look_x, look_y) in field.asteroids:
            return (look_x, look_y)
        look_x, look_y = look_x + x_step, look_y + y_step
    return None


def count_visible(field, location, directions):
    """
    Count how many asteroids are visible from a given location in a field.
    """
    return sum(
        1 for direction in directions if raycast(field, location, direction) is not None
    )


def parse(puzzle_input):
    """
    Parse the puzzle input into a set of asteroid locations.
    """
    rows = puzzle_input.splitlines()
    height = len(rows)
    width = len(rows[0])
    return AsteroidField(
        width,
        height,
        {(x, y) for y in range(height) for x in range(width) if rows[y][x] == "#"},
    )


def part1(field):
    """
    Solve for the answer to part 1.
    """
    directions = get_directions(field.width, field.height)
    loc_info = {
        (x, y): count_visible(field, (x, y), directions)
        for x in range(field.width)
        for y in range(field.height)
    }
    best_loc = max(loc_info.keys(), key=loc_info.__getitem__)
    return loc_info[best_loc], best_loc


def pipe_answer(part1_answer):
    """
    Return the actual answer to part1 and the info passed onto part2.
    """
    return part1_answer


def part2(field, part1_loc):
    """
    Solve for the answer to part 2.
    """
    # TODO: Works perfectly with test case but fails on actual input???
    directions = get_directions(field.width, field.height, order_cw=True)
    dir_idx = directions.index((0, -1))
    destroyed = 0
    while destroyed < 200:
        loc = raycast(field, part1_loc, directions[dir_idx])
        if loc is not None:
            destroyed += 1
            field.asteroids.discard(loc)
        dir_idx = (dir_idx + 1) % len(directions)
    return 100 * loc[0] + loc[1]
