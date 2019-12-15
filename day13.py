"""AdventOfCode2019 - Day 13"""
import collections
import intcode
from day02 import parse

BLOCK_TILE, PLAYER_TILE, BALL_TILE = 1, 3, 4
LEFT, NEUTRAL, RIGHT = -1, 0, 1


class Game:
    """Class to represent the game state."""

    def __init__(self, program):
        self.tiles = collections.defaultdict(int)
        self.interpretor = intcode.Interpretor()
        self.program = program
        self.score = 0
        self.player_x = 0
        self.ball_x = 0

    def run(self):
        """Run the game using self.choose_move."""
        while self.interpretor.run(self.program):
            for x_pos, y_pos, tile_id in self.interpretor.output(group_size=3):
                if (x_pos, y_pos) == (-1, 0):
                    self.score = tile_id
                else:
                    self.draw(x_pos, y_pos, tile_id)
            if self.interpretor.waiting_input():
                self.interpretor.receive_input(self.choose_move())

    def choose_move(self):
        """Decide whether to move left or move right or do nothing."""
        if self.ball_x > self.player_x:
            return RIGHT
        if self.ball_x < self.player_x:
            return LEFT
        return NEUTRAL

    def draw(self, x_pos, y_pos, tile_id):
        """Draw a tile to the screen."""
        self.tiles[x_pos, y_pos] = tile_id
        if tile_id == PLAYER_TILE:
            self.player_x = x_pos
        if tile_id == BALL_TILE:
            self.ball_x = x_pos


def part1(program):
    """Solve for the answer to part 1."""
    game = Game(program)
    game.run()
    return sum(value == BLOCK_TILE for value in game.tiles.values())


def part2(program):
    """Solve for the ansewr to part 2."""
    program[0] = 2  # put in 2 quarters
    game = Game(program)
    game.run()
    return game.score
