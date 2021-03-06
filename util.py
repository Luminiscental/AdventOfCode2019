"""General utility functions for all days."""
import collections
import functools
import operator
import math
import inspect
import time
import contextlib
import itertools


def tuple_add(tup1, tup2):
    """Add two tuples component-wise."""
    return tuple(map(operator.add, tup1, tup2))


def tuple_sub(tup1, tup2):
    """Subtract two tuples component-wise."""
    return tuple(map(operator.sub, tup1, tup2))


def tuple_scale(tup1, scalar):
    """Multiply the components of a tuple."""
    return tuple(map(lambda elem: elem * scalar, tup1))


def adjacent_2d_tuples(position):
    """Create a generator yielding the adjacent positions, where positions are (x, y) tuples."""
    for offset in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        yield tuple_add(position, offset)


def dijkstra(nodes, edge_producer, start_node, end_node):
    """Perform dijkstra's algorithm, returning a distance or math.inf if no path is found."""
    dists = collections.defaultdict(lambda: math.inf)
    dists[start_node] = 0
    unvisited = set(nodes)
    while unvisited:
        curr = min(unvisited, key=dists.__getitem__)
        curr_dist = dists[curr]
        if curr_dist == math.inf:
            break
        for adj, dist in edge_producer(curr):
            new_dist = curr_dist + dist
            if new_dist < dists[adj]:
                dists[adj] = new_dist
        unvisited.discard(curr)
    return dists[end_node]


def bfs(
    traversable_pred,
    start_node,
    adj_node_producer=adjacent_2d_tuples,
    end_node=None,
    initial_state=None,
    state_updater=lambda pos, dist, state: state,
):
    """Perform BFS, optionally with a state that updates along each step of the path, and
    optionally finding a path to a specific target.
    """
    Node = collections.namedtuple("Node", "pos dist state")
    queue = collections.deque([Node(start_node, 0, initial_state)])
    visited = set([start_node])
    while queue:
        curr = queue.popleft()
        if end_node is not None and curr.pos == end_node:
            return curr.dist, curr.state
        new_state = state_updater(curr.pos, curr.dist, curr.state)
        visited.add(curr.pos)
        for adj_node in adj_node_producer(curr.pos):
            if adj_node not in visited and traversable_pred(adj_node):
                queue.append(Node(adj_node, curr.dist + 1, new_state))
    if end_node is not None:
        raise ValueError("No path found")
    return new_state


def replace_occurences(sequence, subsequence, replacement):
    """Replace occurences of a subsequence in a sequence."""
    while True:
        for i in range(len(sequence)):
            if sequence[i : i + len(subsequence)] == subsequence:
                sequence[i : i + len(subsequence)] = replacement
                break
        else:
            break


def count_occurences(sequence, subsequence):
    """Count occurences of a subsequence in a sequence."""
    return ilen(
        i
        for i in range(len(sequence))
        if sequence[i : i + len(subsequence)] == subsequence
    )


def ilen(iterable):
    """Count the length of an iterable."""
    return sum(1 for _ in iterable)


def ilast(iterable):
    """Return the last value yielded by an iterable, or None."""
    item = None
    for item in iterable:
        pass
    return item


@contextlib.contextmanager
def timer(desc):
    """Context manager for timing a block of code once and printing the time."""
    start = time.time()
    yield
    end = time.time()
    print(f"{desc}: took {end - start:0.5f} seconds")


def apply_trim_args(func, *args):
    """Apply a function to given arguments, using only as many as required."""
    arg_count = len(inspect.signature(func).parameters)
    return func(*args[:arg_count])


def combinations(sequence, min_size=None, max_size=None):
    """Yield all combinations of elements from a finite sequence."""
    if min_size is None:
        min_size = 0
    if max_size is None:
        max_size = len(sequence)
    for count in range(min_size, max_size + 1):
        yield from itertools.combinations(sequence, count)


def repeat_each(iterable, count):
    """Make an iterator repeating every element of an iterable a given number of times."""
    for elem in iterable:
        for _ in range(count):
            yield elem


def chunks_of(size, iterable):
    """Split an iterable into a list of lists of the given size."""
    args = [iter(iterable)] * size
    return [list(chunk) for chunk in zip(*args)]


def chain_lengths(values):
    """Returns a generator of the lengths of chains of repeated values in a sequence."""
    return (ilen(group) for _, group in itertools.groupby(values))


def sign(number):
    """Return the sign of an integer (-1, 0, 1)."""
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def lcm(num1, num2):
    """Return the lowest common multiple of a pair of integers."""
    return num1 * num2 // math.gcd(num1, num2)


def lcm_all(numbers):
    """Return the lowest common multiple of a sequence of integers."""
    return functools.reduce(lcm, numbers)
