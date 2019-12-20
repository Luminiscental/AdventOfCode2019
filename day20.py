"""AdventOfCode2019 - Day 20"""
import collections
import operator
from util import adjacent_2d_tuples, bfs
from day18 import parse


def label_for(fst_letter, snd_letter, direction):
    """Get the label for a portal given the encountered letters and direction."""
    # If we went left or up reverse it
    return (
        f"{snd_letter}{fst_letter}" if -1 in direction else f"{fst_letter}{snd_letter}"
    )


def find_portals(maze):
    """Find the location and label for every portal entrance in the maze."""
    # portals[label] = (inner_entrance, outer_entrance)
    portals = {}
    # Look at every point in the maze
    for pos, tile in maze.items():
        # If it's traversable look at everything adjacent to it
        if tile == ".":
            for offset in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                adj = tuple(map(operator.add, pos, offset))
                adj_tile = maze[adj]
                # If it's the start of a label find the whole label
                if adj_tile.isupper():
                    next_pos = tuple(map(operator.add, adj, offset))
                    next_tile = maze[next_pos]
                    assert next_tile.isupper(), "ill-formed label found"
                    after_pos = tuple(map(operator.add, next_pos, offset))
                    is_outer = after_pos not in maze
                    label = label_for(adj_tile, next_tile, offset)
                    # Store the position that the portal was adjacent to
                    portals.setdefault(label, [None, None])[int(is_outer)] = pos
    return portals


def part1(maze, state):
    """Solve for the answer to part 1."""
    portals = find_portals(maze)
    portal_pairs = state["portal_pairs"] = [
        (inner, outer) for inner, outer in portals.values() if inner is not None
    ]
    _, start = portals["AA"]
    _, end = portals["ZZ"]
    state["start"], state["end"] = start, end

    def get_adj(pos):
        for inner, outer in portal_pairs:
            if pos == inner:
                yield outer
            if pos == outer:
                yield inner
        for adj in adjacent_2d_tuples(pos):
            yield adj

    distance, _ = bfs(
        start_node=start,
        traversable_pred=lambda pos: maze[pos] == ".",
        adj_node_producer=get_adj,
        end_node=end,
    )
    return distance


def part2(maze, state):
    """Solve for the answer to part 2."""
    portal_pairs = state["portal_pairs"]
    start = state["start"]
    end = state["end"]

    def get_adj(node):
        for inner, outer in portal_pairs:
            if node.lvl > 0 and node.pos == outer:
                yield Node(pos=inner, lvl=node.lvl - 1)
            if node.pos == inner:
                yield Node(pos=outer, lvl=node.lvl + 1)
        for adj in adjacent_2d_tuples(node.pos):
            yield Node(pos=adj, lvl=node.lvl)

    Node = collections.namedtuple("Node", "pos lvl")
    distance, _ = bfs(
        start_node=Node(pos=start, lvl=0),
        traversable_pred=lambda node: maze[node.pos] == ".",
        adj_node_producer=get_adj,
        end_node=Node(pos=end, lvl=0),
    )
    return distance
