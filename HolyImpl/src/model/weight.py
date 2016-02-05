class Weight:
    def __init__(self, length=1, homology=[], leafmost=1):
        self.length = length
        self.homology = homology
        self.leafmost = leafmost

    def __cmp__(self, other):
        assert isinstance(other, Weight)
        return cmp((self.length, self.homology, self.leafmost), \
                   (other.length, other.homology, other.leafmost))
