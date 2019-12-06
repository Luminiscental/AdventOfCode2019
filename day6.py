"""
AdventOfCode2019 - Day 6
"""
from collections import defaultdict


def parse(puzzle_input):
    """
    Parse the puzzle input into a directed graph of the orbiting objects.
    Taking advantage of the non-cyclical nature.
    """
    graph = defaultdict(set)
    for line in puzzle_input.splitlines():
        system = line.split(")")
        orbited = system[0]
        orbitor = system[1]
        graph[orbited].add(orbitor)
    return graph


def count_orbitors(graph, root):
    """
    Count the direct and indirect orbitors of an object.
    """
    orbit_count = 0
    objects_to_count = [root]
    while objects_to_count:
        curr = objects_to_count.pop()
        orbitors = graph[curr]
        for orbitor in orbitors:
            orbit_count += 1
            objects_to_count.append(orbitor)
    return orbit_count


def part1(graph):
    """
    Solve for the answer to part 1.
    """
    result = 0
    # Have to make a list copy of the keys because defaultdict might mutate in iteration
    for obj in list(graph.keys()):
        result += count_orbitors(graph, obj)
    return result


def part2(graph):
    """
    Solve for the answer to part 2.
    """
