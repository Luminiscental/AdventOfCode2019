"""AdventOfCode2019 - Day 20"""
import collections
from util import bfs, dijkstra, tuple_add
from day18 import parse

Portal = collections.namedtuple("Portal", "label is_inner")


def flip_portal(portal):
    """Flip from inner to outer portal or vice versa."""
    return Portal(label=portal.label, is_inner=not portal.is_inner)


def label_for(fst_letter, snd_letter, direction):
    """Get the label for a portal given the encountered letters and direction."""
    # If we went left or up reverse it
    return (
        f"{snd_letter}{fst_letter}" if -1 in direction else f"{fst_letter}{snd_letter}"
    )


def find_portals(maze):
    """Find each inner and outer portal."""
    # inner_portals[inner_location] = label
    inner_portals = {}
    # outer_portals[outer_location] = label
    outer_portals = {}

    # Look at every point in the maze
    for pos, tile in maze.items():
        # If it's traversable look at everything adjacent to it
        if tile == ".":
            for offset in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                adj = tuple_add(pos, offset)
                adj_tile = maze[adj]
                # If it's the start of a label find the whole label
                if adj_tile.isupper():
                    next_pos = tuple_add(adj, offset)
                    next_tile = maze[next_pos]
                    assert next_tile.isupper(), "ill-formed label found"
                    after_pos = tuple_add(next_pos, offset)
                    label = label_for(adj_tile, next_tile, offset)
                    if after_pos in maze:
                        inner_portals[pos] = label
                    else:
                        outer_portals[pos] = label
    return inner_portals, outer_portals


def find_distances(maze, inner_portals, outer_portals):
    """Calculate the distances between each portal using BFS."""
    distances = collections.defaultdict(dict)

    def update(pos, dist, state):
        if pos in inner_portals:
            portal = Portal(label=inner_portals[pos], is_inner=True)
            if state != portal:
                distances[state][portal] = dist
        elif pos in outer_portals:
            portal = Portal(label=outer_portals[pos], is_inner=False)
            if state != portal:
                distances[state][portal] = dist
        return state

    for inner, label in inner_portals.items():
        bfs(
            traversable_pred=lambda pos: maze[pos] == ".",
            start_node=inner,
            state_updater=update,
            initial_state=Portal(label, is_inner=True),
        )
    for outer, label in outer_portals.items():
        bfs(
            traversable_pred=lambda pos: maze[pos] == ".",
            start_node=outer,
            state_updater=update,
            initial_state=Portal(label, is_inner=False),
        )
    return distances


def part1(maze, state):
    """Solve for the answer to part 1."""
    inner_portals, outer_portals = find_portals(maze)
    distances = state["distances"] = find_distances(maze, inner_portals, outer_portals)
    start_portal = state["start_portal"] = Portal(label="AA", is_inner=False)
    end_portal = state["end_portal"] = Portal(label="ZZ", is_inner=False)

    def get_edges(portal):
        # Walking edges
        yield from distances[portal].items()
        # Teleporting edges
        if portal.label not in ("AA", "ZZ"):
            yield flip_portal(portal), 1

    return dijkstra(
        nodes=distances.keys(),
        edge_producer=get_edges,
        start_node=start_portal,
        end_node=end_portal,
    )


def part2(_, state):
    """Solve for the answer to part 2."""
    distances = state["distances"]
    start_portal = state["start_portal"]
    end_portal = state["end_portal"]

    Node = collections.namedtuple("Node", "portal level")

    def get_edges(node):
        # Walking edges
        for portal, dist in distances[node.portal].items():
            yield Node(portal, node.level), dist
        # Teleporting edges
        if node.portal.label not in ("AA", "ZZ"):
            if node.portal.is_inner:
                yield Node(flip_portal(node.portal), node.level + 1), 1
            elif node.level > 0:
                yield Node(flip_portal(node.portal), node.level - 1), 1

    # Assume the shortest path doesn't go beyond level 50
    max_level = 50
    return dijkstra(
        nodes={
            Node(portal, level)
            for portal in distances.keys()
            for level in range(max_level + 1)
        },
        edge_producer=get_edges,
        start_node=Node(start_portal, level=0),
        end_node=Node(end_portal, level=0),
    )
