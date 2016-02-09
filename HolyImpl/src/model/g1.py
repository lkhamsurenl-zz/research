from src.model.dart import Dart
from src.model.edge import Edge
from src.model.vertex import Vertex
from src.model.weight import Weight
from src.model.graph import Graph

__author__ = 'Luvsandondov Lkhamsuren'

class G1(Graph):
    # genus 1 grid of 3 x 3
    def __init__(self):
        # Build vertices and faces.
        vertices, faces = [[None for j in range(3)] for i in range(3)], [[None for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                vertices[i][j] = Vertex((i, j))
                faces[i][j] = Vertex((i, j))

        # Build darts and duals
        ae = Edge(vertices[0][0], vertices[0][2], Weight(1, [-1,0], 0), faces[0][2], faces[2][2])
        bf = Edge(vertices[1][0], vertices[1][2], Weight(1, [-1,0], 6), faces[1][2], faces[0][2])
        cg = Edge(vertices[2][0], vertices[2][2], Weight(1, [-1,0], 4), faces[2][2], faces[1][2])

        ca = Edge(vertices[2][0], vertices[0][0], Weight(1, [0,-1], 0), faces[2][0], faces[2][2])
        ge = Edge(vertices[2][2], vertices[0][2], Weight(1, [0,-1], -3), faces[2][2], faces[2][1])
        kd = Edge(vertices[2][1], vertices[0][1],  Weight(1, [0,-1], -1), faces[2][1], faces[2][0])

        ab = Edge(vertices[0][0], vertices[1][0], Weight(1, [0,0], -8), faces[0][0], faces[0][2])
        bc = Edge(vertices[1][0], vertices[2][0], Weight(1, [0,0], 1), faces[1][0], faces[1][2])
        ef = Edge(vertices[0][2], vertices[1][2], Weight(1, [0,0], -1), faces[0][2], faces[0][1])

        fg = Edge(vertices[1][2], vertices[2][2], Weight(1, [0,0], 0), faces[1][2], faces[1][1])
        dh = Edge(vertices[0][1], vertices[1][1], Weight(1, [0,0], 0), faces[0][1], faces[0][0])
        hk = Edge(vertices[1][1], vertices[2][1], Weight(1, [0,0], 0), faces[1][1], faces[1][0])

        ed = Edge(vertices[0][2], vertices[0][1], Weight(1, [0,0], 0), faces[0][1], faces[2][1])
        fh = Edge(vertices[1][2], vertices[1][1], Weight(1, [0,0], 0), faces[1][1], faces[0][1])
        gk = Edge(vertices[2][2], vertices[2][1], Weight(1, [0,0], -1), faces[2][1], faces[1][1])

        da = Edge(vertices[0][1], vertices[0][0], Weight(1, [0,0], 0), faces[0][0], faces[2][0])
        hb = Edge(vertices[1][1], vertices[1][0], Weight(1, [0,0], 0), faces[1][0], faces[0][0])
        kc = Edge(vertices[2][1], vertices[2][0], Weight(1, [0,0], 0), faces[2][0], faces[1][0])

        self.vertices = sum(vertices, [])
        self.faces = sum(faces, [])