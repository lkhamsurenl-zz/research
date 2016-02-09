import copy

from src.model.vertex import Vertex
from src.model.weight import Weight

__author__ = 'Luvsandondov Lkhamsuren'

class Dart:
    def __init__(self, tail, head, weight, left=None, right=None):
        """
        Create dart
        :param tail: Tail vertex
        :param head: Head vertex
        :param left: Left face
        :param right: Right face
        :param weight: Weight of the dart.
        :return:
        """
        assert(isinstance(head, Vertex))
        assert(isinstance(tail, Vertex))
        #assert(isinstance(left, Vertex))
        #assert(isinstance(right, Vertex))
        assert(isinstance(weight, Weight))

        self.head = head
        self.tail = tail
        self.left = left
        self.right = right
        self.weight = weight

        self.reverse = None
        self.dual = None
        self.tail.add_dart(head, self)

    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def create_reverse_dart(self):
        # Reverse dart has negated homology and leafmost terms.
        reverse_weight = Weight(length=self.weight.length, homology=[-h for h in self.weight.homology], \
                                leafmost=-self.weight.leafmost)
        return Dart(self.head, self.tail, reverse_weight, self.right, self.left)

    def create_dual_dart(self):
        return Dart(self.left, self.right, copy.deepcopy(self.weight), self.tail, self.head)

    def __str__(self):
        return "{} -> {}; weight: {}".format(self.tail, self.head, self.weight)
