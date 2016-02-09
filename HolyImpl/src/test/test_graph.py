from unittest import TestCase

from src.algorithms.traversal import bfs
from src.model.graph import Graph
from src.model.vertex import Vertex
from src.model.grid import grid
from src.model.g1 import G1

class TestGraph(TestCase):
    def test_add_vertex(self):
        a = Vertex("a")
        b = Vertex("b")
        a.add_dart(b, 1)

        g = Graph([a, b])
        g.add_vertex("c")
        self.assertTrue(len(g.vertices) == 3)

    def test_remove_vertex(self):
        a = Vertex("a")
        b = Vertex("b")
        a.add_dart(b, 1)

        g = Graph([a, b])
        g.remove_vertex("a")
        self.assertTrue(len(g.vertices) == 1)

