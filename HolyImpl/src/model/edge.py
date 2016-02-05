from src.model.dart import Dart

__author__ = 'Luvsandondov Lkhamsuren'

class Edge:
    """
    Edge includes two darts (reverse of each other) as tuple (dart1, dart2)
    """
    def __init__(self, dart1, dart2):
        assert(isinstance(dart1, Dart))
        assert(isinstance(dart2, Dart))

        self.darts = (dart1, dart2)

    def get_dual(self):
        # TODO(lkhamsurenl): Return dual edge.
        return NotImplemented