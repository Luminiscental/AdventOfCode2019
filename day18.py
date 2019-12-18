"""AdventOfCode2019 - Day 18"""
import collections
import operator
import functools

Path = collections.namedtuple("Path", "end dist doors keys")
Tour = collections.namedtuple("Tour", "pos keys")


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
    doors = {pos for pos, tile in maze.items() if tile.isupper()}
    key_for = {
        door_pos: key_pos
        for key_pos in keys
        for door_pos in doors
        if maze[door_pos] == maze[key_pos].upper()
    }
    paths = {}

    def mark_paths(start_pos):
        """Mark the distances and passed doors/keys to every door/key given a starting position."""
        # Use BFS
        queue = collections.deque(
            [Path(end=start_pos, dist=0, doors=frozenset(), keys=frozenset())]
        )
        visited = set([start_pos])
        while queue:
            curr = queue.popleft()
            next_doors, next_keys = curr.doors, curr.keys
            if curr.end in (keys | doors) and curr.dist > 0:
                paths[start_pos, curr.end] = curr
                next_doors |= {curr.end} & doors
                next_keys |= {curr.end} & keys
            visited.add(curr.end)
            for offset in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                adj_pos = tuple(map(operator.add, curr.end, offset))
                if maze[adj_pos] != "#" and adj_pos not in visited:
                    queue.append(Path(adj_pos, curr.dist + 1, next_doors, next_keys))

    mark_paths(start)
    for pos in keys:
        mark_paths(pos)

    @functools.lru_cache(maxsize=None)
    def shortest_tour(start, unlocked=frozenset()):
        """Find the shortest path from a starting position to get all keys."""
        # Use DFS
        remaining = keys - unlocked
        if not remaining:
            return 0
        return min(
            path.dist + shortest_tour(path.end, unlocked | path.keys | {path.end})
            for path in [paths[start, key] for key in remaining]
            if all(key_for[door] in unlocked for door in path.doors)
        )

    return shortest_tour(start)


def part2(maze):
    """Solve for the answer to part 2."""
