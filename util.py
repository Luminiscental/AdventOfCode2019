"""
General utility functions for all days.
"""

import requests


def get_input(day_number):
    """
    Get the puzzle input for the given day.
    """
    with open(".cookie", "r") as cookie_file:
        cookie = cookie_file.read().strip()
        return requests.get(
            f"https://adventofcode.com/2019/day/{day_number}/input",
            cookies={"session": cookie},
        ).text
