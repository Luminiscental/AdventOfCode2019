"""
AdventOfCode2019 - Day 8
"""

WIDTH = 25
HEIGHT = 6


def chunks_of(size, iterable):
    """
    Iterate in chunks of a given size.
    """
    args = [iter(iterable)] * size
    return [list(chunk) for chunk in zip(*args)]


def display_image(image):
    """
    Return a human readable string to display the binary image.
    """
    return "\n".join(
        "".join("#" if pixel else " " for pixel in row)
        for row in chunks_of(WIDTH, image)
    )


def parse(puzzle_input):
    """
    Parse the puzzle input.
    """
    pixels = [int(c) for c in puzzle_input if c != "\n"]
    layers = chunks_of(WIDTH * HEIGHT, pixels)
    return list(reversed(layers))


def part1(layers):
    """
    Solve for the answer to part 1.
    """
    layer = min(layers, key=lambda layer: layer.count(0))
    return layer.count(1) * layer.count(2)


def part2(layers):
    """
    Solve for the answer to part 2.
    """
    final_image = layers[-1]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = -2
            while final_image[x + y * WIDTH] == 2:
                final_image[x + y * WIDTH] = layers[idx][x + y * WIDTH]
                idx -= 1
    return display_image(final_image)
