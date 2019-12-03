"""
AdventOfCode2019 - Day 3
"""

import math


class Point:
    """
    A mutable 2D point.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def transpose(self):
        """
        Return the transpose of this point.
        """
        return Point(self.y, self.x)

    def distance(self, other):
        """
        Return the distance to another point.
        """
        diff = Point(self.x - other.x, self.y - other.y)
        return math.sqrt(diff.x ** 2 + diff.y ** 2)


class Line:
    """
    Represents a line on the grid, parametrized by start point, length, and whether it's
    horizontal or vertical. The direction is always positive (up or right) from the start point.
    """

    def __init__(self, start, length, horizontal):
        self.start = start
        self.length = length
        self.horizontal = horizontal
        if self.horizontal:
            self.end = Point(self.start.x + self.length, self.start.y)
        else:
            self.end = Point(self.start.x, self.start.y + self.length)

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def xrange(self):
        """
        Return the range of x-values spanned by this line.
        """
        return range(self.start.x, self.end.x + 1)

    def yrange(self):
        """
        Return the range of y-values spanned by this line.
        """
        return range(self.start.y, self.end.y + 1)

    def transpose(self):
        """
        Return the transpose of this line.
        """
        return Line(self.start.transpose(), self.length, not self.horizontal)

    def intersections(self, other):
        """
        Return a list of points of intersection between this and another line in the grid.
        """
        # Transpose to only deal with the case where self is horizontal:
        if not self.horizontal:
            return [
                point.transpose()
                for point in self.transpose().intersections(other.transpose())
            ]
        # Parrallel case:
        if other.horizontal:
            if self.start.y != other.start.y:
                return []
            # Collinear case:
            start = max(self.start.x, other.start.x)
            end = min(self.end.x, other.end.x)
            return [Point(x, self.start.y) for x in range(start, end + 1)]
        # Perpendicular case:
        xintersect = other.start.x
        yintersect = self.start.y
        if xintersect not in self.xrange() or yintersect not in other.yrange():
            return []
        return [Point(xintersect, yintersect)]


def parse_wire(string):
    """
    Parse an ordered list of lines from a string of directions.
    """
    lines = []
    cursor = Point(0, 0)
    directions = string.split(",")
    for elem in directions:
        direction = elem[0]
        distance = int(elem[1:])
        if direction == "L":
            line_cursor = Point(cursor.x - distance, cursor.y)
            lines.append(Line(line_cursor, distance, True))
            cursor.x -= distance
        elif direction == "R":
            line_cursor = Point(cursor.x, cursor.y)
            lines.append(Line(line_cursor, distance, True))
            cursor.x += distance
        elif direction == "D":
            line_cursor = Point(cursor.x, cursor.y - distance)
            lines.append(Line(line_cursor, distance, False))
            cursor.y -= distance
        elif direction == "U":
            line_cursor = Point(cursor.x, cursor.y)
            lines.append(Line(line_cursor, distance, False))
            cursor.y += distance
        else:
            raise ValueError(f"Unknown direction '{direction}'")
    return lines


def parse(puzzle_input):
    """
    Parse the input into a list of lines for each wire.
    """
    return [parse_wire(wire_line) for wire_line in puzzle_input.splitlines()]


def part1(wires):
    """
    Solve for the answer to part 1.
    """
    intersections = set()
    for line1 in wires[0]:
        for line2 in wires[1]:
            intersections.update(line1.intersections(line2))
    distances = [point.x + point.y for point in intersections if point != Point(0, 0)]
    return min(distances)


def part2(wires):
    """
    Solve for the answer to part 2.
    """
    intersections = set()
    steps1 = 0
    for line1 in wires[0]:
        steps2 = 0
        for line2 in wires[1]:
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
            steps2 = steps2 + line2.length
        steps1 = steps1 + line1.length
    intersection, dist1, dist2 = min(intersections, key=lambda tup: tup[1] + tup[2])
    return dist1 + dist2
