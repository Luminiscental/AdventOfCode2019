"""AdventOfCode2019 - Day 18"""
import collections
import operator
import itertools
import functools


class CombDict(dict):
    """Dictionary storing values for key-key pairs."""

    def __getitem__(self, pair):
        assert isinstance(pair, tuple) and len(pair) == 2, "invalid key for CombDict"
        return (
            super().__getitem__(pair)
            if pair in self
            else super().__getitem__(tuple(reversed(pair)))
        )


def get_path(maze, traversable, doors, start, target):
    """Using BFS get the shortest path, returning the distance and the doors traversed."""
    if maze[start] not in traversable:
        raise ValueError("Invalid start position")
    Node = collections.namedtuple("Node", "pos dist doors")
    visited = set([start])
    queue = collections.deque([Node(pos=start, dist=0, doors=set())])
    while queue:
        curr = queue.pop()
        if curr.pos == target:
            return curr.dist, curr.doors
        for offset in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            adjacent = tuple(map(operator.add, curr.pos, offset))
            if maze[adjacent] in traversable | doors and adjacent not in visited:
                queue.append(
                    Node(
                        pos=adjacent,
                        dist=curr.dist + 1,
                        doors=curr.doors | {maze[adjacent]} & doors,
                    )
                )
                visited.add(adjacent)
    raise ValueError(f"No path found for {maze[start]} to {maze[target]}")


def parse(puzzle_input):
    """Parse the puzzle input into a dict of (x, y): tile."""
    return {
        (x, y): tile
        for y, row in enumerate(puzzle_input.splitlines())
        for x, tile in enumerate(row)
    }


def part1(maze):
    """Solve for the answer to part 1."""
    assert list(maze.values()).count("@") == 1, "start position ambiguous"
    start = next(pos for pos, tile in maze.items() if tile == "@")
    keys = {pos for pos, tile in maze.items() if tile.islower()}
    key_names = {maze[key] for key in keys}
    door_names = set(map(str.upper, key_names))
    dist_dict = CombDict()
    block_dict = CombDict()
    for key1, key2 in itertools.combinations(keys, 2):
        dist_dict[key1, key2], block_dict[key1, key2] = get_path(
            maze,
            traversable={".", "@"} | key_names,
            doors=door_names,
            start=key1,
            target=key2,
        )
    accessible = {}
    for key in keys:
        dist, blocked = get_path(
            maze,
            traversable={".", "@"} | key_names,
            doors=door_names,
            start=start,
            target=key,
        )
        if not blocked:
            accessible[key] = dist

    @functools.lru_cache(maxsize=None)
    def shortest_from(key, unlocked=frozenset()):
        unlocked = unlocked | {key}
        if keys == unlocked:
            return 0
        unlocked_doors = {maze[key].upper() for key in unlocked}
        return min(
            dist_dict[key, other_key] + shortest_from(other_key, unlocked)
            for other_key in keys - unlocked
            if all(door in unlocked_doors for door in block_dict[key, other_key])
        )

    return min(dist + shortest_from(key) for key, dist in accessible.items())


def part2(maze):
    """Solve for the answer to part 2."""
