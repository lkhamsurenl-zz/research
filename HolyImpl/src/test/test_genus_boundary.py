from unittest import TestCase

from src.view.genus_boundary import get_vertex_mapping, resolve_boundary_darts
from sets import Set

class TestGenusBoundary(TestCase):
    def test_vertex_mapping_g1(self):
        g = 1
        m, n = 3, 3
        vertex_mapping = get_vertex_mapping(g, m, n)

        correct_mapping = {
            (0, 0): [(0, 0), (3, 0), (0, 3), (3, 3)],
            (0, 1): [(0, 1), (3, 1)],
            (0, 2): [(0, 2), (3, 2)],
            (1, 0): [(1, 0), (1, 3)],
            (2, 0): [(2, 0), (2, 3)]
        }

        # All the internal nodes should have only itself as boundary duplicate.
        for i in range(1, m):
            for j in range(1, n):
                correct_mapping[(i, j)] = [(i, j)]

        for v in vertex_mapping:
            assert Set(vertex_mapping[v]) == Set(correct_mapping[v]), \
                "vertex_mapping_g1({}) = {}; want: {}".format(v, vertex_mapping[v], correct_mapping[v])

    def test_vertex_mapping_g2(self):
        g = 2
        m, n = 6, 6
        vertex_mapping = get_vertex_mapping(g, m, n)

        correct_mapping = {
            (0, 0): [(0, 0), (3, 0), (6, 0), (0, 3), (3, 6), (0, 6), (6, 3), (6, 6)],
            (0, 1): [(0, 1), (6, 4)],
            (0, 2): [(0, 2), (6, 5)],
            (0, 4): [(0, 4), (6, 1)],
            (0, 5): [(0, 5), (6, 2)],
            (1, 0): [(1, 0), (4, 6)],
            (2, 0): [(2, 0), (5, 6)],
            (4, 0): [(4, 0), (1, 6)],
            (5, 0): [(5, 0), (2, 6)]
        }

        # All the internal nodes should have only itself as boundary duplicate.
        for i in range(m):
            for j in range(n):
                if (i, j) not in correct_mapping:
                    correct_mapping[(i, j)] = [(i, j)]
                else:
                    correct_mapping[(i, j)] += [(i, j)]

        for v in vertex_mapping:
            assert Set(vertex_mapping[v]) == Set(correct_mapping[v]), \
                "vertex_mapping_g2({}) = {}; want: {}".format(v, vertex_mapping[v], correct_mapping[v])
