"""
AdventOfCode2019 - Day 6
"""

from collections import defaultdict


class Tree:
    """
    A tree where nodes can have any number of children.
    """

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.parent = None

    def __iter__(self):
        for node in self.children:
            yield node
            for child in node:
                yield child

    def find(self, value):
        """
        Check whether a value is contained in the tree, returning None if not.
        """
        if self.value == value:
            return {"node": self, "steps": 0}
        for child in self.children:
            found = child.find(value)
            if found is not None:
                return {"node": found["node"], "steps": 1 + found["steps"]}
        return None

    def find_skipping(self, value, skipped_child):
        """
        Check whether a value is contained in the tree discounting one child.
        """
        self.children.discard(skipped_child)
        result = self.find(value)
        self.children.add(skipped_child)
        return result

    def set_parents(self):
        """
        Set the parent field of all child nodes.
        """
        for child in self.children:
            child.set_parents()
            child.parent = self

    def find_ancestor_with(self, other_value):
        """
        Find the lowest common ancestor with another node specified by its value. Returns None if
        the node is not in the tree.
        """
        ancestor = self
        steps_up = 0
        while ancestor is not None:
            found = ancestor.find(other_value)
            if found is not None:
                return {"node": found["node"], "up": steps_up, "down": found["steps"]}
            ancestor = ancestor.parent
            steps_up += 1
        return None

    @staticmethod
    def from_dict(parent_dict, root):
        """
        Create a tree from a dictionary from parent value to child values.
        """
        return Tree(
            root, {Tree.from_dict(parent_dict, child) for child in parent_dict[root]}
        )


def parse(puzzle_input):
    """
    Parse the puzzle input into a dictionary of parent to children in the tree.
    """
    parent_dict = defaultdict(set)
    for line in puzzle_input.splitlines():
        system = line.split(")")
        orbited = system[0]
        orbitor = system[1]
        parent_dict[orbited].add(orbitor)
    tree = Tree.from_dict(parent_dict, "COM")
    tree.set_parents()
    return tree


def part1(tree):
    """
    Solve for the answer to part 1.
    """
    # Slow recursive iteration, not sure how to improve
    return sum(1 + sum(1 for _ in node) for node in tree)


def part2(tree):
    """
    Solve for the answer to part 2.
    """
    found = tree.find("YOU")
    if found is None:
        raise ValueError("Input didn't contain a YOU node")
    you = found["node"]

    common = you.find_ancestor_with("SAN")
    if common is None:
        raise ValueError("Input didn't contain a SAN node")

    return common["up"] + common["down"] - 2
