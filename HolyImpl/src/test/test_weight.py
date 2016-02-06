from unittest import TestCase
from src.model.weight import Weight

class TestWeight(TestCase):

    def test_weight_compare(self):
        # Weight comparison 1st component.
        w1 = Weight(1, [2,1,1], 1)
        w2 = Weight(2, [1,1,1], 1)
        self.assertTrue(w1 < w2)

        # Compare Homology.
        w3 = Weight(1, [2,1,1], 1)
        w4 = Weight(1, [1,2,1], 2)
        self.assertTrue(w3 > w4)

        # Compare leafmost.
        w5 = Weight(1, [1,1,1], 2)
        w6 = Weight(1, [1,1,1], 1)
        self.assertTrue(w5 > w6)

    def test_weight_add(self):
        w1 = Weight(1, [2,1,1], 1)
        w2 = Weight(2, [1,1,1], 1)

        self.assertEqual(w1 + w2, Weight(3, [3,2,2], 2))

    def test_weight_sub(self):
        w1 = Weight(1, [2,1,1], 1)
        w2 = Weight(2, [1,1,1], 1)

        self.assertEqual(w2 - w1, Weight(1, [-1,0,0], 0))
