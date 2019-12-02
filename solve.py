"""
Main module for running the solution for a given day.
"""

import sys

import util


def main():
    """
    Main entry point; runs a day based on command line input.
    """
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <day number>")
        sys.exit(1)
    day_num = int(sys.argv[1])
    util.run_day(day_num)


if __name__ == "__main__":
    main()
