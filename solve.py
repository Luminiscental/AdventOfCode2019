"""
Main module for running the solution for a given day.
"""

import sys

import util


def main():
    """
    Main entry point; runs a day based on command line input.
    """
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <day number>")
        sys.exit(1)
    for day_num in (int(arg) for arg in sys.argv[1:]):
        print(f"day {day_num}:")
        util.run_day(day_num)
        print()


if __name__ == "__main__":
    main()
