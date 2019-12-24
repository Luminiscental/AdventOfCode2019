"""AdventOfCode2019 - Day 17"""
import collections
import operator
import intcode
from util import count_occurences, replace_occurences, ilast, tuple_add
from day02 import parse

DIRECTIONS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
TURNS = {
    "L": {"<": "v", "^": "<", ">": "^", "v": ">"},
    "R": {"<": "^", "^": ">", ">": "v", "v": "<"},
}
Robot = collections.namedtuple("Robot", "pos facing")


def find_programs(path):
    """Find a set of programs to execute a path that fit in memory.
    :param path: expected as a list of each (turn,distance) instruction.
    :return: a tuple (main, program A, program B, program C).
    """
    subpath_names = ["A", "B", "C"]
    subpaths = {}

    def subpath_quality(subpath):
        # If it overlaps a previous subpath we don't want it
        if any(elem in subpath_names for elem in subpath):
            return 0
        # Otherwise take the one that appears most often
        return count_occurences(path, subpath)

    for subpath_name in subpath_names:
        # Start at the first non-covered instruction
        start = next(i for i, elem in enumerate(path) if elem not in subpath_names)
        # Choose the best subpath of length 3-6 (reversed to prefer longer paths)
        candidates = (path[start : start + length] for length in reversed(range(3, 6)))
        best_subpath = max(candidates, key=subpath_quality)
        # Substitute the subpath into path
        replace_occurences(path, best_subpath, [subpath_name])
        # Record the subpath
        subpaths[subpath_name] = best_subpath

    assert all(elem in subpath_names for elem in path), "could not find a coverage"
    return (path, *subpaths.values())


def find_path(scaffolds, robot):
    """Find a path to cover a set of scaffolds.
    :param scaffolds: expected as a set of (x, y) tuples representing where the scaffolds are.
    :param robot: the initial robot state.
    :return: a list of instruction strings like "L,13".
    """
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
        next_pos = tuple_add(curr_pos, DIRECTIONS[curr_facing])
        # If we can keep going without turning, do so
        if next_pos in scaffolds:
            steps += 1
            curr_pos = next_pos
        else:
            if last_turn is not None:
                path.append(f"{last_turn},{steps}")
                steps = 0
            else:
                assert steps == 0, "didn't  turn initially"
            # Find the first direction we can turn in
            for turn_name, turn in TURNS.items():
                turn_facing = turn[curr_facing]
                turn_pos = tuple_add(curr_pos, DIRECTIONS[turn_facing])
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
    """Queue input to submit a sequence of programs to the robot.
    :param interpretor: the intcode interpretor to queue as input for.
    :param programs: expected as a sequence of programs, where each program is a list of string
    instructions. The instructions are comma delimited and newline terminated by this function,
    then converted to ascii and queued as input to the program.
    """
    for program in programs:
        assembled = [ord(c) for c in ",".join(program) + "\n"]
        assert len(assembled) <= 20, "Program was too long"
        interpretor.queue_inputs(assembled)


def interpret_image(image_string):
    """Parse the image to the set of scaffolds and initial robot state.
    :param image_string: expected as the program output joined to a string.
    :return: a tuple (robot, scaffolds) with the initial robot state and scaffolds set.
    """
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
    """Calculate the alignment sum for a set of scaffolds."""
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
    # Run the program to collect all the output
    interpretor = intcode.Interpretor()
    image_string = "".join(chr(code) for code in interpretor.run(program))
    state["robot"], state["scaffolds"] = interpret_image(image_string)
    return calibrate(state["scaffolds"])


def part2(program, state):
    """Solve for the answer to part 2."""
    path = find_path(state["scaffolds"], state["robot"])
    programs = find_programs(path)
    interpretor = intcode.Interpretor()
    queue_programs(interpretor, [*programs, "n"])
    program[0] = 2
    return ilast(interpretor.run(program))
