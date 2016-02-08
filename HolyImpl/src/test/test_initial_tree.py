from unittest import TestCase

from src.algorithms import initial_holy_tree
from src.model.g1 import G1

class TestInitialTree(TestCase):
    def test_holy_tree(self):
        g1 = G1()
        # Source vertex.
        vertex = g1.get_vertex((1, 1))
        (fast_pred, fast_dist) = initial_holy_tree.fast_initial_tree(g1, vertex)
        (slow_pred, slow_dist) = initial_holy_tree.fast_initial_tree(g1, vertex)

        self.assertEqual(fast_pred, slow_pred)
        self.assertEqual(fast_dist, slow_dist)

