"""AdventOfCode2019 - Day 19"""
import itertools
import intcode
from day02 import parse


class Drone:
    """Class handling the drone state / output."""

    def __init__(self, program):
        self.program = program
        self.interpretor = intcode.Interpretor()
        self.rows = {0: (0, 1)}  # self.rows[y] = (start, end) of beam for row y
        self.find_start()

    def find_start(self):
        """Handle skipping the empty rows after row 0."""
        start_x, start_y = next(
            (x_idx, y_idx)
            for y_idx in itertools.count(start=1)
            # Assume the beam isn't shallower than x = 10y
            for x_idx in range(10 * y_idx)
            if self.force_check(x_idx, y_idx) == 1
        )
        for y_idx in range(1, start_y):
            self.rows[y_idx] = (0, 0)
        self.rows[start_y] = (
            start_x,
            next(
                col
                for col in itertools.count(start_x)
                if self.force_check(col, start_y) == 0
            ),
        )

    def get_x_range(self, y_value):
        """Get the bounds of the tractor beam at a given y value."""
        if y_value not in self.rows:
            prev_start, prev_end = self.rows[y_value - 1]
            # Assume thing decrease nicely
            start = next(
                col
                for col in itertools.count(prev_start)
                if self.force_check(col, y_value) == 1
            )
            end = next(
                col
                for col in itertools.count(max(prev_end, start))
                if self.force_check(col, y_value) == 0
            )
            self.rows[y_value] = (start, end)
        return self.rows[y_value]

    def force_check(self, pos_x, pos_y):
        """Run the program to check a given position for the tractor beam."""
        assert pos_x >= 0 and pos_y >= 0, f"{pos_x},{pos_y} is an invalid position"
        self.interpretor.reset()
        self.interpretor.queue_inputs((pos_x, pos_y))
        return next(self.interpretor.run(self.program))


def part1(program, state):
    """Solve for the answer to part 1."""
    drone = state["drone"] = Drone(program)
    return sum(
        min(x_end, 50) - x_start
        for check_y in range(50)
        for x_start, x_end in [drone.get_x_range(check_y)]
        if x_start < 50
    )


def part2(_, state):
    """Solve for the answer to part 2."""
    drone = state["drone"]
    side_length = 100
    beam_ranges = map(drone.get_x_range, itertools.count())
    # List of candidate top-left corners
    candidates = []
    for row, (start, end) in enumerate(beam_ranges):
        if end - start < side_length:
            continue
        new_candidates = [(end - side_length, row)]
        for cand_x, cand_y in candidates:
            if cand_x >= start:
                if row - cand_y == side_length - 1:
                    return 10000 * cand_x + cand_y
                new_candidates.append((cand_x, cand_y))
        candidates = new_candidates
    raise ValueError("Infinite loop ended")
