"""AdventOfCode2019 - Day 10"""
import collections
import math
import operator

AsteroidField = collections.namedtuple("AsteroidField", "width height asteroids")


def get_directions(width, height):
    """Get a list of the x and y steps for every direction within the region, ordered clockwise."""
    result = [
        (x_step, y_step)
        for x_step in range(1 - width, width)
        for y_step in range(1 - height, height)
        if math.gcd(x_step, y_step) == 1
    ]
    # upside down coordinates so atan2 actually goes clockwise
    result.sort(key=lambda direction: math.atan2(direction[1], direction[0]))
    return result


def raycast(field, location, direction):
    """Return the position of the first asteroid hit, or None."""
    x_step, y_step = direction
    loc_x, loc_y = location
    look_x, look_y = loc_x + x_step, loc_y + y_step
    while 0 <= look_x < field.width and 0 <= look_y < field.height:
        if (look_x, look_y) in field.asteroids:
            return (look_x, look_y)
        look_x, look_y = look_x + x_step, look_y + y_step
    return None


def count_visible(field, location, directions):
    """Count how many asteroids are visible from a given location in a field."""
    return sum(
        1 for direction in directions if raycast(field, location, direction) is not None
    )


def parse(puzzle_input):
    """Parse the puzzle input into a set of asteroid locations."""
    rows = puzzle_input.splitlines()
    height = len(rows)
    width = len(rows[0])
    return AsteroidField(
        width,
        height,
        {(x, y) for y in range(height) for x in range(width) if rows[y][x] == "#"},
    )


def part1(field, state):
    """Solve for the answer to part 1."""
    state["directions"] = directions = get_directions(field.width, field.height)

    loc_info = {
        asteroid: count_visible(field, asteroid, directions)
        for asteroid in field.asteroids
    }
    station_loc, visible_count = max(loc_info.items(), key=operator.itemgetter(1))
    state["station"] = station_loc
    return visible_count


def part2(field, state):
    """Solve for the answer to part 2."""
    station_loc = state["station"]
    directions = state["directions"]

    dir_idx = directions.index((0, -1))
    destroyed = 0
    while destroyed < 200:
        loc = raycast(field, station_loc, directions[dir_idx])
        if loc is not None:
            destroyed += 1
            field.asteroids.discard(loc)
        dir_idx = (dir_idx + 1) % len(directions)
    return 100 * loc[0] + loc[1]
