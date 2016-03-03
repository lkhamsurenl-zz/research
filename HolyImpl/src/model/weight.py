class Weight:
    def __init__(self, length=0, homology=[], leafmost=0):
        self.length = length
        self.homology = homology
        self.leafmost = leafmost

    def __cmp__(self, other):
        if other == None:
            return 1
        assert isinstance(other, Weight)
        return cmp((self.length, self.homology, self.leafmost), \
                   (other.length, other.homology, other.leafmost))

    def __neg__(self):
        return Weight(-self.length, [-i for i in self.homology], -self.leafmost)

    def __add__(self, other):
        return Weight(self.length + other.length, [i + j for (i, j) in zip(self.homology, other.homology)], \
                                     self.leafmost + other.leafmost)

    def __sub__(self, other):
        return Weight(self.length - other.length, [i - j for (i, j) in zip(self.homology, other.homology)], \
                                     self.leafmost - other.leafmost)
    def __str__(self):
        return "<{0},{1},{2}>".format(self.length, self.homology, self.leafmost)
