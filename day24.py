"""AdventOfCode2019 - Day 24"""
from util import adjacent_2d_tuples

# tile: set(tiles adjacent to tile in inner layer)
ADJACENT_INNER = {
    (1, 2): {(0, idx) for idx in range(5)},
    (3, 2): {(4, idx) for idx in range(5)},
    (2, 1): {(idx, 0) for idx in range(5)},
    (2, 3): {(idx, 4) for idx in range(5)},
}

# tile: set(tiles adjacent to tile in outer layer)
ADJACENT_OUTER = {
    outer: set(inner for inner in ADJACENT_INNER if outer in ADJACENT_INNER[inner])
    for outer in set.union(*ADJACENT_INNER.values())
}


def valid(tile):
    """Check if an index pair is within the board."""
    return tile[0] in range(5) and tile[1] in range(5)


def alive(tile, board):
    """Check if a tile is alive given the board state"""
    return valid(tile) and board[tile[0] + 5 * tile[1]]


def count_neighbours(board, tile):
    """Count the neighbouring bugs to a tile."""
    return sum(alive(neighbour, board) for neighbour in adjacent_2d_tuples(tile))


def count_layered_neighbours(layer, inner, outer, tile):
    """Count the neighbouring bugs to a tile including from neighbouring layers."""
    total = count_neighbours(layer, tile)
    if inner is not None and tile in ADJACENT_INNER:
        total += sum(alive(adj, inner) for adj in ADJACENT_INNER[tile])
    if outer is not None and tile in ADJACENT_OUTER:
        total += sum(alive(adj, outer) for adj in ADJACENT_OUTER[tile])
    return total


def alive_next(bug, neighbours):
    """Check whether a tile is alive next given its current neighbours and state."""
    if bug:
        return neighbours == 1
    if neighbours in (1, 2):
        return True
    return bug


def step_board(board):
    """Return the next board state."""
    return tuple(
        alive_next(alive((x, y), board), count_neighbours(board, (x, y)))
        for y in range(5)
        for x in range(5)
    )


def step_layer(layer, inner, outer):
    """Return the next state of a layer given its outer and inner neighbour layers."""
    return tuple(
        (x, y) != (2, 2)  # ignore the center tile
        and alive_next(
            alive((x, y), layer), count_layered_neighbours(layer, inner, outer, (x, y))
        )
        for y in range(5)
        for x in range(5)
    )


def step_layers(layers):
   # flat neighbours   """Return the next layer states."""
    # Add padding for bugs to expand into
    layers.append([False] * 5 * 5)
    layers.insert(0, [False] * 5 * 5)
    # Step all the layers
    result_middle = [
        step_layer(layer, inner, outer)
        for outer, layer, inner in zip(layers, layers[1:], layers[2:])
    ]
    result_start = [step_layer(layers[0], inner=layers[1], outer=None)]
    result_end = [step_layer(layers[-1], inner=None, outer=layers[-2])]
    return result_start + result_middle + result_end


def biodiversity(board):
    """Calculate the biodiversity of a board state."""
    return sum(2 ** idx if bug else 0 for idx, bug in enumerate(board))


def bug_count(layers):
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
        state = step_board(state)
    return biodiversity(state)


def part2(initial_state):
    """Solve for the answer to part 2."""
    layers = [initial_state]
    for _ in range(200):
        layers = step_layers(layers)
    return bug_count(layers)
