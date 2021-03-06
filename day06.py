"""AdventOfCode2019 - Day 6"""
import collections
import functools


class Tree:
    """A tree where nodes can have any number of children."""

    def __init__(self, value, children, parent=None):
        self.value = value
        self.children = children
        self.parent = parent

    def __iter__(self):
        for child in self.children:
            yield child
            yield from child

    @functools.lru_cache(maxsize=None)
    def find(self, value):
        """Check whether a value is contained in the tree, returning None if not."""
        if self.value == value:
            return {"node": self, "steps": 0}
        for child in self.children:
            found = child.find(value)
            if found is not None:
                return {"node": found["node"], "steps": 1 + found["steps"]}
        return None

    def set_parents(self):
        """Set the parent field of all child nodes."""
        for child in self.children:
            child.set_parents()
            child.parent = self

    def find_ancestor_with(self, other_value):
        """Find the lowest common ancestor with another node.
        Returns None if there is no node with other_value found in the same tree.
        """
        ancestor = self
        steps_up = 0
        while ancestor is not None:
            # double checks ancestor each time, could improve
            found = ancestor.find(other_value)
            if found is not None:
                return {"node": found["node"], "up": steps_up, "down": found["steps"]}
            ancestor = ancestor.parent
            steps_up += 1
        return None

    @staticmethod
    def from_dict(parent_dict, root):
        """Create a tree from a dictionary of parent values to child value iterables."""
        result = Tree(
            root, {Tree.from_dict(parent_dict, child) for child in parent_dict[root]}
        )
        result.set_parents()
        return result


def parse(puzzle_input):
    """Parse the puzzle input into a dictionary of nodes to children."""
    parent_dict = collections.defaultdict(set)
    for line in puzzle_input.splitlines():
        orbited, orbitor = line.split(")")
        parent_dict[orbited].add(orbitor)
    return parent_dict


def part1(parent_dict):
    """Solve for the answer to part 1."""

    @functools.lru_cache(maxsize=None)
    def count_paths(parent):
        # using sum() is noticeably slower than this for loop
        result = 0
        for child in parent_dict[parent]:
            result += 1 + count_paths(child)
        return result

    return sum(map(count_paths, list(parent_dict.keys())))


def part2(parent_dict):
    """Solve for the answer to part 2."""
    tree = Tree.from_dict(parent_dict, "COM")
    found = tree.find("YOU")
    if found is None:
        raise ValueError("Input didn't contain a YOU node")
    you = found["node"]
    common = you.find_ancestor_with("SAN")
    if common is None:
        raise ValueError("Input didn't contain a SAN node")
    return common["up"] + common["down"] - 2
