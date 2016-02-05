from unittest import TestCase
from src.model.vertex import Vertex

class TestVertex(TestCase):
    # TODO(lkhamsurenl): Add before method to refactor duplicate vertex creation.
    def test_add_dart(self):
        a = Vertex("a")
        b = Vertex("b")
        a.add_dart(b, 1)
        self.assertTrue(len(a.neighbors) != 0)
        self.assertTrue(len(b.neighbors) == 0)

    def test_is_neighbor(self):
        a = Vertex("a")
        b = Vertex("b")
        a.add_dart(b, 1)
        self.assertTrue(a.is_neighbor(b))
        self.assertFalse(b.is_neighbor(a))

    def test_remove_dart(self):
        a = Vertex("a")
        b = Vertex("b")
        a.add_dart(b, 1)
        # Remove the dart
        a.remove_dart(b)
        self.assertFalse(a.is_neighbor(b))