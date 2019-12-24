"""AdventOfCode2019 - Day 24"""
from util import adjacent_2d_tuples


def alive(tile, board):
    """Check if a tile is alive given the board state"""
    return board[tile[0] + 5 * tile[1]]


def display_board(board):
    """Return a human readable string for the board state."""
    return "\n".join(
        "".join("#" if alive((x, y), board) else "." for x in range(5))
        for y in range(5)
    )


def valid(tile):
    """Check if an index pair is within the board."""
    return tile[0] in range(5) and tile[1] in range(5)


def count_neighbours(board, tile):
    """Count the neighbouring bugs to a tile."""
    return sum(
        1
        for neighbour in adjacent_2d_tuples(tile)
        if valid(neighbour) and alive(neighbour, board)
    )


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


def biodiversity(board):
    """Calculate the biodiversity of a board state."""
    return sum(2 ** idx if bug else 0 for idx, bug in enumerate(board))


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
