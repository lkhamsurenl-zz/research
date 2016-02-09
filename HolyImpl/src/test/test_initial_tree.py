from unittest import TestCase

import time

import sys

from src.algorithms import initial_holy_tree
from src.model.g1 import G1
from src.model.grid import grid

class TestInitialTree(TestCase):
    def test_holy_tree(self):
        g1 = G1()
        # Source vertex.
        vertex = g1.get_vertex((1, 1))
        (fast_pred, fast_dist) = initial_holy_tree.fast_initial_tree(g1, vertex)
        (slow_pred, slow_dist) = initial_holy_tree.fast_initial_tree(g1, vertex)

        self.assertEqual(fast_pred, slow_pred)
        self.assertEqual(fast_dist, slow_dist)

    def test_initial_tree_with_grid(self):
        # NOTE(lkhamsurenl): Following line is needed if copying graph is too deep, when using copy.deepcopy
        # sys.setrecursionlimit(10000)
        
        graph_1 = grid(10, 10)
        # Source vertex.
        vertex = graph_1.get_vertex((1, 1))
        fast_start = time.time()
        (fast_pred, fast_dist) = initial_holy_tree.fast_initial_tree(graph_1, vertex)
        fast_end = time.time()
        (slow_pred, slow_dist) = initial_holy_tree.slow_initial_tree(graph_1, vertex)
        slow_end = time.time()
        print("fast: {}, slow: {}".format(fast_end - fast_start, slow_end - fast_end))

        self.assertEqual(fast_pred, slow_pred)
        self.assertEqual(fast_dist, slow_dist)
