from src.model.dart import Dart
from src.model.edge import Edge
from src.model.graph import Graph
from src.model.vertex import Vertex
from src.model.weight import Weight


class G1(Graph):
    def grid(self, m, n):
        """
        Create m x n grid graph with genus 1.
        1st row and last column are the homology cycles.
        Bottom left face is the MSSP face with top right vertex of this face being the first source.
        :param m:
        :param n:
        :return:
        """
        vs = []
        for i in range(m):
            for j in range(n):
                vs.append(Vertex((i, j)))

        for i in range(m):
            for j in range(n):
                v = vs[i][j]
                # Add offset to find 4 neighbors.
                for x in range(-1,2):
                    for y in range(-1, 2):
                        if (x + y) != 0:
                            neighbor = vs[(i + x) % n][(j + y) % n]
                            if i == m - 1 and x == 1:
                                Edge(v, neighbor, Weight(1, [0,-1], 0))
                            elif j == n - 1 and y == 1:
                                Edge(v, neighbor, Weight(1, [1,0], 0))
                            else:
                                Edge(v, neighbor, Weight(1, [0, 0], 0))
        Edge(vs[m-1][0], vs[0][0], Weight(1, [0,-1], 0))
        Edge(vs[0][n-1], vs[0][0], Weight(1, [1,0], 0))
        # TODO(lkhamsurenl): Update leafmost terms.

        self.vertices = vs
        # TODO(lkhamsurenl): Create faces and connect duals.
        self.faces = []