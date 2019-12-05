"""
General utility functions for all days.
"""

import sys
import requests

import day1
import day2
import day3
import day4
import day5


def get_input(day_number):
    """
    Get the puzzle input for the given day.
    """
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
    """
    Solve and print the answer for a given day.
    """
    puzzle_input = get_input(day_num)
    day_module = [day1, day2, day3, day4, day5][day_num - 1]
    parsed_input = day_module.parse(puzzle_input)
    part1 = day_module.part1(parsed_input)
    print(f"part1: {part1}")
    part2 = day_module.part2(parsed_input)
    print(f"part2: {part2}")
