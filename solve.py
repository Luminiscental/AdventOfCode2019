"""Main module for running the solution for a given day."""
import sys
import importlib
import requests
from util import timer, apply_trim_args


def day_module_name(day_num):
    """Get the module name for a given day number."""
    return f"day{day_num:02}"


def has_day(day_num):
    """Return whether a module is available for a given day."""
    return importlib.util.find_spec(day_module_name(day_num)) is not None


def get_input(day_number):
    """Get the puzzle input for the given day as a string."""
    try:
        with open(".cookie", "r") as cookie_file:
            cookie = cookie_file.read().strip()
            return requests.get(
                f"https://adventofcode.com/2019/day/{day_number}/input",
                cookies={"session": cookie},
            ).text
    except FileNotFoundError:
        print(
            "Could not find .cookie file to get input from adventofcode.com, "
            "input is user-dependent so I need your session id"
        )
        sys.exit(1)


def run_day(day_num):
    """Solve and print the answers for a given day."""
    print(f"Day {day_num}")
    with timer("downloading input"):
        puzzle_input = get_input(day_num)
    day_module = importlib.import_module(day_module_name(day_num))
    day_state = {}
    with timer("parsing input"):
        parsed_input = apply_trim_args(day_module.parse, puzzle_input, day_state)
    with timer("running part 1"):
        part1 = apply_trim_args(day_module.part1, parsed_input, day_state)
    with timer("running part 2"):
        part2 = apply_trim_args(day_module.part2, parsed_input, day_state)
    print()
    print(f"part1:\n\n{part1}\n")
    print(f"part2:\n\n{part2}\n")
    print()


def main():
    """Main entry point; runs a day based on command line input."""
    if len(sys.argv) < 2:
        print(f"usage: python {sys.argv[0]} [<day numbers> | all]")
        print(
            "example:\n"
            + f"$ python {sys.argv[0]} 1 # solves day 1\n"
            + f"$ python {sys.argv[0]} 2 5 # solves days 2 and 5\n"
            + f"$ python {sys.argv[0]} all # solves all days in the repo\n"
        )
        sys.exit(1)
    with timer("overall"):
        if sys.argv[1:] == ["all"]:
            day_num = 1
            while has_day(day_num):
                run_day(day_num)
                day_num += 1
        else:
            for day_num in (int(arg) for arg in sys.argv[1:]):
                run_day(day_num)
    sys.exit(0)


if __name__ == "__main__":
    main()
