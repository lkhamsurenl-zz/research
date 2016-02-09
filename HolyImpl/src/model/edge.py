from src.model.dart import Dart
from src.model.vertex import Vertex
import copy

__author__ = 'Luvsandondov Lkhamsuren'

class Edge:
    """
    Edge includes two darts (reverse of each other) as tuple (dart1, dart2)
    """
    def __init__(self, source, destination, weight, left=None, right=None):
        assert(isinstance(source, Vertex))
        assert(isinstance(destination, Vertex))
        assert(isinstance(left, Vertex))
        assert(isinstance(right, Vertex))

        # Creating darts will add it to the
        dart1 = Dart(source, destination, weight, left, right)
        dart2 = dart1.create_reverse_dart()
        dart1.reverse = dart2
        dart2.reverse = dart1

        dual1 = dart1.create_dual_dart()
        dual2 = dual1.create_reverse_dart()
        dual1.reverse = dual2
        dual2.reverse = dual1

        dart1.dual = dual1
        dart2.dual = dual2
        dual1.dual = dart1
        dual2.dual = dart2