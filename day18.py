"""AdventOfCode2019 - Day 18"""
import collections
import operator
import itertools
import functools

Path = collections.namedtuple("Path", "end dist doors keys")
Tour = collections.namedtuple("Tour", "pos keys")


def parse(puzzle_input):
    """Parse the puzzle input into a dict of (x, y): tile character."""
    return {
        (x, y): tile
        for y, row in enumerate(puzzle_input.splitlines())
        for x, tile in enumerate(row)
    }


def mark_paths(maze, start_pos, keys, doors, paths):
    """Calculate the length and passed keys/doors of the shortest paths from start_pos to every
    other key/door, assuming all the relevant doors are open. The results are written to paths
    as paths[start, end] = Path(...).
    """
    # Use BFS
    queue = collections.deque(
        [Path(end=start_pos, dist=0, doors=frozenset(), keys=frozenset())]
    )
    visited = set([start_pos])
    while queue:
        curr = queue.popleft()
        next_doors, next_keys = curr.doors, curr.keys
        # If we've found a key/door after moving store our path
        if curr.end in (keys | doors) and curr.dist > 0:
            paths[start_pos, curr.end] = curr
            # Add the key/door to the child paths
            next_doors |= {curr.end} & doors
            next_keys |= {curr.end} & keys
        visited.add(curr.end)
        # Spawn child paths where there isn't a wall
        for offset in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            adj_pos = tuple(map(operator.add, curr.end, offset))
            if maze[adj_pos] != "#" and adj_pos not in visited:
                queue.append(Path(adj_pos, curr.dist + 1, next_doors, next_keys))


def part1(maze, state):
    """Solve for the answer to part 1."""
    assert list(maze.values()).count("@") == 1, "start position ambiguous"
    # Get some data out of the maze
    start = state["start"] = next(pos for pos, tile in maze.items() if tile == "@")
    keys = state["keys"] = {pos for pos, tile in maze.items() if tile.islower()}
    doors = state["doors"] = {pos for pos, tile in maze.items() if tile.isupper()}
    key_for = state["key_for"] = {
        door_pos: key_pos
        for key_pos in keys
        for door_pos in doors
        if maze[door_pos] == maze[key_pos].upper()
    }

    # Mark the shortest paths ignoring doors from each key and the start position
    paths = {}
    mark_paths(maze, start, keys, doors, paths)
    for key in keys:
        mark_paths(maze, key, keys, doors, paths)

    # Find the shortest tour, assuming that each segment is a shortest path if you ignore doors.
    # This assumption holds because the inputs we get have simple paths between the keys.
    @functools.lru_cache(maxsize=None)
    def shortest_tour(start, unlocked=frozenset()):
        """Find the shortest path from a starting position to get all keys."""
        remaining = keys - unlocked
        if not remaining:
            return 0
        # Brute force all the places we could go next, thank you lru_cache
        return min(
            path.dist + shortest_tour(path.end, unlocked | path.keys | {path.end})
            for path in [paths[start, key] for key in remaining]
            if all(key_for[door] in unlocked for door in path.doors)
        )

    return shortest_tour(start)


def part2(maze, state):
    """Solve for the answer to part 2."""
    # Section the maze and add the robots
    replacement = ["@#@", "###", "@#@"]
    start = state["start"]
    for x_offset, y_offset in itertools.product((-1, 0, 1), repeat=2):
        maze_idx = tuple(map(operator.add, start, (x_offset, y_offset)))
        maze[maze_idx] = replacement[y_offset + 1][x_offset + 1]

    # The strategy here is basically the same as part 1, only slight change in the DFS

    # Get some data out of the maze
    robots = frozenset(pos for pos, tile in maze.items() if tile == "@")
    keys = state["keys"]
    doors = state["doors"]
    key_for = state["key_for"]

    # Mark the shortest paths similar to part 1, but including all 4 start positions now
    paths = {}
    for robot in robots:
        mark_paths(maze, robot, keys, doors, paths)
    for key in keys:
        mark_paths(maze, key, keys, doors, paths)

    @functools.lru_cache(maxsize=None)
    def shortest_tour(robots, unlocked=frozenset()):
        """Find the shortest number of steps to get all keys."""
        # Use DFS
        remaining = keys - unlocked
        if not remaining:
            return 0
        # Brute force all the places each robot could go next, thank you lru_cache
        return min(
            path.dist
            + shortest_tour(
                robots - {mover} | {path.end}, unlocked | path.keys | {path.end},
            )
            for mover in robots
            for path in [
                paths[mover, key] for key in remaining if (mover, key) in paths
            ]
            if all(key_for[door] in unlocked for door in path.doors)
        )

    return shortest_tour(robots)
