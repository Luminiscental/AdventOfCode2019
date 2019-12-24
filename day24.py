"""AdventOfCode2019 - Day 24"""
import math
from util import adjacent_2d_tuples, tuple_add, tuple_sub, tuple_scale, sign


def alive(tile, board):
    """Check if a tile is alive given the board state"""
    return board[tile[0] + 5 * tile[1]]


def display_board(board):
    """Return a human readable string for the board state."""
    return "\n".join(
        "".join("#" if alive((x, y), board) else "." for x in range(5))
        for y in range(5)
    )


def display_layers(layers):
    return "\n\n".join(display_board(layer) for layer in layers)


def valid(tile):
    """Check if an index pair is within the board."""
    return tile[0] in range(5) and tile[1] in range(5)


def count_neighbours(board, tile):
    """Count the neighbouring bugs to a tile."""
    return sum(
        valid(neighbour) and alive(neighbour, board)
        for neighbour in adjacent_2d_tuples(tile)
    )


def middle_bugs(board, direction):
    """Count the bugs neighbouring the middle in a given direction."""
    offsets = [direction] if 0 in direction else [(direction[0], 0), (0, direction[1])]
    return sum(alive(tuple_add((2, 2), offset), board) for offset in offsets)


def edge_bugs(board, direction):
    """Count the bugs on the edge in a given direction."""
    # Assumes direction is 0 in one component
    if direction[0] == 0:
        center_line = ((idx, 2) for idx in range(5))
    else:
        center_line = ((2, idx) for idx in range(5))
    tiles = (
        tuple_add(center_point, tuple_scale(direction, 2))
        for center_point in center_line
    )
    return sum(alive(tile, board) for tile in tiles)


def layered_neighbours(tile, layer, inner=None, outer=None):
    """Count the neighbouring bugs to a tile on a layer given the inner and outer layers,
    or None if they are empty.
    """
    flat_neighbours = count_neighbours(layer, tile)
    tile_offset = tuple_sub(tile, (2, 2))  # offset from center
    tile_dir = tuple(map(sign, tile_offset))
    if 2 in tile_offset or -2 in tile_offset:  # outer neighbours
        if outer is None:
            adj_neighbours = 0
        else:
            adj_neighbours = middle_bugs(
                outer, tuple(map(lambda x: math.trunc(x / 2), tile_offset))
            )
    else:  # inner neighbours
        if inner is None or 0 not in tile_dir:  # on diagonals there are no adjacents
            adj_neighbours = 0
        else:
            adj_neighbours = edge_bugs(inner, tuple(map(sign, tile_offset)))
    return flat_neighbours + adj_neighbours


def alive_next(bug, neighbours):
    """Check whether a tile is alive next given its current neighbours and state."""
    if bug:
        return neighbours == 1
    if neighbours in (1, 2):
        return True
    return bug


def step(board):
    """Return the next board state."""
    return tuple(
        alive_next(bug, count_neighbours(board, (idx % 5, idx // 5)))
        for idx, bug in enumerate(board)
    )


def step_layer(layer, inner=None, outer=None):
    """Step a layer state given its inner and outer layers, None if they are empty."""
    return tuple(
        idx != 12
        and alive_next(
            bug, layered_neighbours((idx % 5, idx // 5), layer, inner, outer)
        )
        for idx, bug in enumerate(layer)
    )


def step_layers(layers):
    """Return the next layer states, modifies layers but leaves it in an equivalent state."""
    # Add blank layers to expand into
    layers.insert(0, [False] * 5 * 5)
    layers.append([False] * 5 * 5)
    # Step layers in the middle
    result = [
        step_layer(layer, inner, outer)
        for outer, layer, inner in zip(layers, layers[1:], layers[2:])
    ]
    # Step the layers on either end
    result.insert(0, step_layer(layers[0], inner=layers[1], outer=None))
    result.append(step_layer(layers[-1], inner=None, outer=layers[-2]))
    # If the inner layer wasn't expanded into leave it out
    if not any(result[-1]):
        result.pop()
    return result


def biodiversity(board):
    """Calculate the biodiversity of a board state."""
    return sum(2 ** idx if bug else 0 for idx, bug in enumerate(board))


def count_bugs(layers):
    """Count the number of bugs given the layer states."""
    return sum(bug for layer in layers for bug in layer)


def parse(puzzle_input):
    """Parse the puzzle input into a tuple of tile states."""
    return tuple(
        char == "#"
        for y, row in enumerate(puzzle_input.splitlines())
        for x, char in enumerate(row)
    )


def part1(initial_state):
    """Solve for the answer to part 1."""
    states = set()
    state = initial_state
    while state not in states:
        states.add(state)
        state = step(state)
    return biodiversity(state)


def part2(initial_state):
    """Solve for the answer to part 2."""
    layers = [initial_state]
    for _ in range(200):
        layers = step_layers(layers)
    return count_bugs(layers)
