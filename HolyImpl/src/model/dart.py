from src.model.vertex import Vertex
from src.model.weight import Weight

__author__ = 'Luvsandondov Lkhamsuren'

class Dart:
    def __init__(self, tail, head, weight):
        assert(isinstance(head, Vertex))
        assert(isinstance(tail, Vertex))
        assert(isinstance(weight, Weight))

        self.head = head
        self.tail = tail
        self.weight = weight
        self.tail.add_dart(head, self)

    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def create_reverse_dart(self):
        # Reverse dart has negated homology and leafmost terms.
        reverse_weight = Weight(length=self.weight.length, homology=[-h for h in self.weight.homology], \
                                leafmost=-self.weight.leafmost)
        return Dart(self.head, self.tail, reverse_weight)

    def get_dual(self):
        # TODO(lkhamsurenl): Implement to get dual dart.
        return NotImplemented