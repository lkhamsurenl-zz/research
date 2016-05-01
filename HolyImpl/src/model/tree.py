from collections import deque
from src.model.weight import Weight

class Tree:
    """
    Tree defined by predecessor pointers with distances to each node.
    """
    def __init__(self, pred={}, dist={}):
        self.pred = pred
        self.dist = dist

    def __eq__(self, other):
        return self.pred == other.pred and self.dist == other.dist

    def __str__(self):
        # Report pred and dist for the holy tree.
        report = u"\u25bd\u25bd\u25bd Holy Tree \u25bd\u25bd\u25bd\n".encode('utf-8')
        for u in self.pred:
            pu = self.pred[u] if u in self.pred else "(None)"
            dpu = self.dist[self.pred[u]] if (u in self.pred and self.pred[u] in self.dist) else "(None)"
            du = self.dist[u] if u in self.dist else "(None)"
            report += "{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}\n".format(pu, u, dpu, du)
        report += u"\u25b3\u25b3\u25b3 Holy Tree \u25b3\u25b3\u25b3\n".encode('utf-8')

        return report

    def pivot_out(self, pivot_in):
        """
        Find a dart that is pivoting out from the holy tree.
        :param pivot_in: Dart pivotting in.
        :return: pivoting out dart.
        """
        for v in self.pred:
            if self.pred[v] == None:
                continue
            dart = self.pred[v].neighbors[v]
            if pivot_in.head == dart.head:
                return dart
        return None

    def add_subtree(self, source, delta):
        """
        Given a source and distance to add, propagate the distance through the graph.
        :param delta: Value to add to the subtree nodes.
        :param source: Root of the subtree.
        :return: Nothing.
        """
        self.dist[source] += delta
        q = deque()
        q.appendleft(source)
        while len(q) != 0:
            u = q.pop()
            for v in u.neighbors.keys():
                if self.pred[v] is not None and self.pred[v] == u:
                    self.dist[v] = self.dist[u] + u.neighbors[v].weight
                    q.appendleft(v)

    def is_holy_tree(self, grid, title="is_holy_tree()"):
        """
        Check if there is no tense dart in grid graph.
        :param title: Example: Pivot (1, 2) -> (0, 2).
        :param grid:
        :return: Report of any tense dart in the graph.
        """
        report = u"\u25bc\u25bc\u25bc {} \u25bc\u25bc\u25bc\n".format(title).encode('utf-8')
        for u in grid.vertices:
            for v in u.neighbors:
                slack = self.dist[u] + u.neighbors[v].weight - self.dist[v]
                if slack < Weight(homology=[0 for _ in range(2 * grid.genus)]) or \
                        (slack == Weight(homology=[0 for _ in range(2 * grid.genus)]) and self.pred[v] != u):
                    report += "is_holy_tree()={0}->{1} tense; dist[{0}]={2};dist[{1}]={3};weight={4};slack={5}\n".\
                        format(u, v, self.dist[u], self.dist[v], u.neighbors[v].weight, slack)
        report += u"\u25b2\u25b2\u25b2 {} \u25b2\u25b2\u25b2\n".format(" " * len(title)).encode('utf-8')

        return report

    def report_difference(self, other):
        # Report difference between self and other.
        return \
            u"\u25bd\u25bd\u25bd This Tree \u25bd\u25bd\u25bd\n".encode('utf-8') + \
            str(self) + \
            u"\u25b3\u25b3\u25b3 This Tree \u25b3\u25b3\u25b3\n".encode('utf-8') + \
            u"\u25bd\u25bd\u25bd Other Tree \u25bd\u25bd\u25bd\n".encode('utf-8') + \
            str(other) + \
            u"\u25b3\u25b3\u25b3 Other Tree \u25b3\u25b3\u25b3\n".encode('utf-8')

