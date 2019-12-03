"""
AdventOfCode2019 - Day 3
"""

import math


class Point:
    """
    Simple 2D point representation.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other):
        """
        Return the distance from another point.
        """
        xdiff = self.x - other.x
        ydiff = self.y - other.y
        return math.sqrt(xdiff ** 2 + ydiff ** 2)

    def transpose(self):
        """
        Return the transposition of this point.
        """
        return Point(self.y, self.x)


class Line:
    """
    Represents a finite line on the grid.
    """

    def __init__(self, start, distance, horizontal):
        self.start = start
        self.distance = distance
        self.horizontal = horizontal

    def __str__(self):
        end_point = (
            Point(self.start.x + self.distance, self.start.y)
            if self.horizontal
            else Point(self.start.x, self.start.y + self.distance)
        )
        return f"{self.start} -> {end_point}"

    def transpose(self):
        """
        Return the transposition of this line.
        """
        return Line(self.start.transpose(), self.distance, not self.horizontal)

    def intersections(self, other):
        """
        Return a list of points of intersection between this and another line.
        """
        if self.horizontal:
            if other.horizontal:
                # Parrallel case:
                if self.start.y != other.start.y:
                    return []

                # Collinear case:
                start = max(self.start.x, other.start.x)
                end = min(self.start.x + self.distance, other.start.x + other.distance)
                return [Point(x, self.start.y) for x in range(start, end + 1)]

            # Perpendicular case:
            xstart = self.start.x
            xend = self.start.x + self.distance
            ystart = other.start.y
            yend = other.start.y + other.distance

            xintersect = other.start.x
            yintersect = self.start.y

            if xintersect not in range(xstart, xend + 1) or yintersect not in range(
                ystart, yend + 1
            ):
                return []

            return [Point(xintersect, yintersect)]
        # Delegate to the other case by transposing
        return [
            point.transpose()
            for point in self.transpose().intersections(other.transpose())
        ]


class Wire:
    """
    A wire on the grid.
    """

    def __init__(self, lines):
        self.lines = lines

    @staticmethod
    def from_string(string):
        """
        Parse the wire from a comma separated string of directions.
        """
        lines = []
        start = Point(0, 0)
        directions = string.split(",")

        for elem in directions:
            direction = elem[0]
            distance = int(elem[1:])

            if direction == "L":
                line_start = Point(start.x - distance, start.y)
                lines.append(Line(line_start, distance, True))
                start.x -= distance
            elif direction == "R":
                line_start = Point(start.x, start.y)
                lines.append(Line(line_start, distance, True))
                start.x += distance
            elif direction == "D":
                line_start = Point(start.x, start.y - distance)
                lines.append(Line(line_start, distance, False))
                start.y -= distance
            elif direction == "U":
                line_start = Point(start.x, start.y)
                lines.append(Line(line_start, distance, False))
                start.y += distance
            else:
                raise ValueError

        return Wire(lines)


def parse(puzzle_input):
    """
    Parse the input into a list of directions for the two wires.
    """
    wires = [Wire.from_string(wire_line) for wire_line in puzzle_input.splitlines()]
    return wires[0], wires[1]


def part1(wire_tuple):
    """
    Solve for the answer to part 1.
    """
    wire1, wire2 = wire_tuple

    intersections = set()
    for line in wire1.lines:
        for line2 in wire2.lines:
            intersections.update(line.intersections(line2))

    distances = [point.x + point.y for point in intersections if point != Point(0, 0)]
    return min(distances)


def part2(wire_tuple):
    """
    Solve for the answer to part 2.
    """
    wire1, wire2 = wire_tuple

    intersections = set()

    steps1 = 0
    for line1 in wire1.lines:

        steps2 = 0
        for line2 in wire2.lines:

            for intersection in line1.intersections(line2):
                if intersection == Point(0, 0):
                    continue
                intersections.add(
                    (
                        intersection,
                        steps1 + int(intersection.distance(line1.start)),
                        steps2 + int(intersection.distance(line2.start)),
                    )
                )

            steps2 = steps2 + line2.distance

        steps1 = steps1 + line1.distance

    intersection, dist1, dist2 = min(intersections, key=lambda tup: tup[1] + tup[2])
    return dist1 + dist2
