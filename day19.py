"""AdventOfCode2019 - Day 19"""
import itertools
import intcode
from day02 import parse


class Drone:
    """Class handling the drone state / output."""

    def __init__(self, program):
        self.program = program
        self.interpretor = intcode.Interpretor()
        self.columns = {}

    def get_y_range(self, x_value):
        """Get the bounds of the tractor beam at a given x value."""
        if x_value not in self.columns:
            start = None
            # Assume the tractor beam doesn't go below y=2x+2
            for row in range(2 + x_value * 2):
                output = self.force_check(x_value, row)
                if start is None and output == 1:
                    start = row
                elif start is not None and output == 0:
                    self.columns[x_value] = (start, row)
                    break
            # No beam in this column
            else:
                assert start is None, "beam went lower than expected"
                self.columns[x_value] = (0, 0)
        return self.columns[x_value]

    def force_check(self, pos_x, pos_y):
        """Run the program to check a given position for the tractor beam."""
        self.interpretor.queue_inputs((pos_x, pos_y))
        while self.interpretor.run(self.program):
            pass
        return next(self.interpretor.output())


def part1(program, state):
    """Solve for the answer to part 1."""
    drone = state["drone"] = Drone(program)
    return sum(
        y_end - y_start
        for check_x in range(50)
        for y_start, y_end in [drone.get_y_range(check_x)]
    )


def part2(_, state):
    """Solve for the answer to part 2."""
    drone = state["drone"]
    side_length = 100
    beam_ranges = map(drone.get_y_range, itertools.count())
    # List of candidate top-left corners
    candidates = []
    for x_idx, (start, end) in enumerate(beam_ranges):
        if end - start < side_length:
            if x_idx % 10 == 0:
                print(f"continuing at {x_idx}, length = {end - start}")
            continue
        new_candidates = [(x_idx, end - side_length)]
        for cand_x, cand_y in candidates:
            if cand_y >= start:
                if x_idx - cand_x == side_length - 1:
                    return 10000 * cand_x + cand_y
                new_candidates.append((cand_x, cand_y))
        candidates = new_candidates
        if x_idx % 10 == 0:
            print(f"checking {x_idx}")
            print(f"candidates are now {candidates}")
    raise ValueError("Infinite loop ended")
