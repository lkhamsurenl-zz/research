from unittest import TestCase

from src.algorithms.traversal import bfs
from src.model.graph import Graph
from src.model.vertex import Vertex
from src.model import grid

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
        c = Vertex("c")
        a.add_dart(b, 1)
        a.add_dart(c, 1)
        b.add_dart(c, 1)

        g = Graph([a, b, c])
        g.remove_vertex("a")
        self.assertTrue(len(g.vertices) == 2)
        self.assertTrue(len(g.get_vertex("b").neighbors) == 1)
        self.assertTrue(len(g.get_vertex("c").neighbors) == 0)
