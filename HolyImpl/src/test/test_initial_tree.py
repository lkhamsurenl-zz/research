from unittest import TestCase

import time
import sys

from src.algorithms import initial_holy_tree
from src.model import grid
from src.model.grid import Grid

class TestInitialTree(TestCase):
    def test_holy_tree(self):
        g1 = grid.g1()
        # Source vertex.
        vertex = g1.get_vertex((1, 1))
        fast_holy_tree = initial_holy_tree.fast_initial_tree(g1, vertex)
        slow_holy_tree = initial_holy_tree.bellman_ford_initial_tree(g1, vertex)

        self.assertEqual(fast_holy_tree, slow_holy_tree)

    def test_initial_tree_with_grid(self):
        # NOTE(lkhamsurenl): Following line is needed if copying graph is too deep, when using copy.deepcopy
        sys.setrecursionlimit(10000)

        grid1 = Grid(1, 10, 10)
        # Source vertex.
        vertex = grid1.get_vertex((1, 1))
        fast_start = time.time()
        fast_holy_tree = initial_holy_tree.fast_initial_tree(grid1, vertex)
        fast_end = time.time()
        slow_holy_tree = initial_holy_tree.bellman_ford_initial_tree(grid1, vertex)
        slow_end = time.time()
        print("g = 1 \n fast: {}, slow: {}".format(fast_end - fast_start, slow_end - fast_end))

        self.assertEqual(fast_holy_tree, slow_holy_tree)

    def test_initial_tree_g2(self):
        # NOTE(lkhamsurenl): Following line is needed if copying graph is too deep, when using copy.deepcopy
        sys.setrecursionlimit(10000)

        grid2 = Grid(2, 6, 6)
        # Source vertex.
        vertex = grid2.get_vertex((1, 1))
        fast_start = time.time()
        fast_holy_tree = initial_holy_tree.fast_initial_tree(grid2, vertex)
        fast_end = time.time()
        slow_holy_tree = initial_holy_tree.bellman_ford_initial_tree(grid2, vertex)
        slow_end = time.time()
        print("g = 2 \n fast: {}, slow: {}".format(fast_end - fast_start, slow_end - fast_end))

        self.assertEqual(fast_holy_tree, slow_holy_tree)
