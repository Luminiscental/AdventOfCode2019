"""AdventOfCode2019 - Day 17"""
import collections
import operator
import intcode
from day02 import parse

DIRECTIONS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
TURNS = {
    "L": {"<": "v", "^": "<", ">": "^", "v": ">"},
    "R": {"<": "^", "^": ">", ">": "v", "v": "<"},
}
Robot = collections.namedtuple("Robot", "pos facing")


def find_programs(path):
    """Find a set of programs to execute a path that fit in memory."""
    # Did by hand...
    main = "A,C,A,B,C,A,B,C,A,B"
    prog_a = "L,12,L,12,L,6,L,6"
    prog_b = "L,12,L,6,R,12,R,8"
    prog_c = "R,8,R,4,L,12"
    return main, prog_a, prog_b, prog_c


def find_path(scaffolds, robot):
    """Find a path to cover a set of scaffolds."""
    curr_pos = robot.pos
    curr_facing = robot.facing
    assert curr_pos in scaffolds, "invalid starting position"
    visited = {curr_pos}
    path = []
    last_turn = None
    steps = 0
    # Assume that naively continuing on the scaffolds gives complete coverage
    while True:
        visited.add(curr_pos)
        next_pos = tuple(map(operator.add, curr_pos, DIRECTIONS[curr_facing]))
        # If we can keep going without turning, do so
        if next_pos in scaffolds:
            steps += 1
            curr_pos = next_pos
        else:
            if last_turn is not None:
                path.append((last_turn, steps))
                steps = 0
            else:
                assert steps == 0, "didn't  turn initially"
            # Find the first direction we can turn in
            for turn_name, turn in TURNS.items():
                turn_facing = turn[curr_facing]
                turn_pos = tuple(map(operator.add, curr_pos, DIRECTIONS[turn_facing]))
                if turn_pos in scaffolds:
                    curr_facing = turn_facing
                    last_turn = turn_name
                    break
            # If we have nowhere to turn the path is done
            else:
                break
    assert visited == scaffolds, "missed some scaffolds"
    return path


def queue_programs(interpretor, programs):
    """Queue input to submit a sequence of programs to the robot."""
    for program in programs:
        assembled = [ord(c) for c in program]
        assert len(assembled) < 20, "Program was too long"
        interpretor.queue_inputs(assembled)
        interpretor.queue_input(ord("\n"))


def interpret_image(image_string):
    """Parse the image to find the scaffolds and robot."""
    scaffolds = set()
    robot = None
    for y_idx, row in enumerate(image_string.splitlines()):
        for x_idx, char in enumerate(row):
            has_robot = char in ("<", ">", "^", "v")
            has_scaffold = has_robot or char == "#"
            if has_robot:
                robot = Robot(pos=(x_idx, y_idx), facing=char)
            if has_scaffold:
                scaffolds.add((x_idx, y_idx))
    return robot, scaffolds


def calibrate(scaffolds):
    """Find the calibrating alignment sum for a set of scaffolds."""
    align_sum = 0
    for scaff_x, scaff_y in scaffolds:
        if all(
            (scaff_x + dx, scaff_y + dy) in scaffolds
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))
        ):
            align_sum += scaff_x * scaff_y
    return align_sum


def part1(program, state):
    """Solve for the answer to part 1."""
    interpretor = intcode.Interpretor()
    while interpretor.run(program):
        pass
    image_string = "".join(chr(code) for code in interpretor.output_queue)
    state["robot"], state["scaffolds"] = interpret_image(image_string)
    return calibrate(state["scaffolds"])


def part2(program, state):
    """Solve for the answer to part 2."""
    path = find_path(state["scaffolds"], state["robot"])
    main, prog_a, prog_b, prog_c = find_programs(path)
    interpretor = intcode.Interpretor()
    queue_programs(interpretor, [main, prog_a, prog_b, prog_c])
    interpretor.queue_input(ord("n"))
    interpretor.queue_input(ord("\n"))
    program[0] = 2
    while interpretor.run(program):
        pass
    return interpretor.output_queue.pop()
