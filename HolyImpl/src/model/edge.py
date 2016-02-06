from src.model.dart import Dart
from src.model.vertex import Vertex

__author__ = 'Luvsandondov Lkhamsuren'

class Edge:
    """
    Edge includes two darts (reverse of each other) as tuple (dart1, dart2)
    """
    def __init__(self, source, destination, weight):
        assert(isinstance(source, Vertex))
        assert(isinstance(destination, Vertex))

        # Creating darts will add it to the
        dart1 = Dart(source, destination, weight)
        dart2 = dart1.create_reverse_dart()

        self.darts = (dart1, dart2)

    def get_dual(self):
        # TODO(lkhamsurenl): Return dual edge.
        return NotImplemented