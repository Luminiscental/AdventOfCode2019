"""
Main module for running the solution for a given day.
"""

import sys

import util


def run_day(day_num):
    """
    Run a day, printing to stdou.
    """
    print(f"Day {day_num}:")
    util.run_day(day_num)
    print()


def main():
    """
    Main entry point; runs a day based on command line input.
    """
    if len(sys.argv) < 2:
        print(f"usage: python {sys.argv[0]} [<day numbers> | all]")
        print(
            "example:\n"
            + f"$ python {sys.argv[0]} 1 # solves day 1\n"
            + f"$ python {sys.argv[0]} 2 5 # solves days 2 and 5\n"
            + f"$ python {sys.argv[0]} all # solves all days in the repo\n"
        )
        sys.exit(1)

    if sys.argv[1:] == ["all"]:
        day_num = 1
        while util.has_day(day_num):
            run_day(day_num)
            day_num += 1
        sys.exit(0)

    for day_num in (int(arg) for arg in sys.argv[1:]):
        run_day(day_num)
    sys.exit(0)


if __name__ == "__main__":
    main()
