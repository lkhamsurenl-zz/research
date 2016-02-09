from unittest import TestCase
from src.model.graph import Graph
from src.model.vertex import Vertex
from src.model.grid import grid

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

    def test_g1(self):
        g1 = grid(4,4)
        # for v in g1.vertices:
        #     for n in v.neighbors.keys():
        #         print("v: {}; reverse: {}; dual: {}".format(v.neighbors[n], v.neighbors[n].reverse, v.neighbors[n].dual))

