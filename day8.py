"""
AdventOfCode2019 - Day 8
"""

WIDTH, HEIGHT = 25, 6

BLACK, WHITE, TRANSPARENT = 0, 1, 2


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
        "".join("#" if pixel == WHITE else " " for pixel in row)
        for row in chunks_of(WIDTH, image)
    )


def parse(puzzle_input):
    """
    Parse the puzzle input into layers.
    """
    pixels = [int(c) for c in puzzle_input if c != "\n"]
    return chunks_of(WIDTH * HEIGHT, pixels)


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
    final_image = [0] * WIDTH * HEIGHT
    for i in range(WIDTH * HEIGHT):
        pixels = [layer[i] for layer in layers]
        final_image[i] = next(pixel for pixel in pixels if pixel != TRANSPARENT)
    return display_image(final_image)
