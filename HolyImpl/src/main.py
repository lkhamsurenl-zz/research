from src.model.graph import Graph
from src.algorithms.holy_tree import move_around_face
import src.model.grid as grid
import sys

#TODO(lkhamsurenl): This should be a final calling method once prototype is done.
def get_face_vertices(graph, names):
    vertices = []
    # Populate all the vertices given their names.
    for name in names:
        vertices.append(graph.get_vertex(name))
    return vertices

def holy_tree():
    sys.setrecursionlimit(10000)
    m, n = 6, 6
    g1 = grid.generate_2d_grid(m, n)
    vertices = get_face_vertices(g1, [(1, 1), (0, 1), (0, 0), (1, 0)])
    move_around_face(g1, m, n, vertices)

holy_tree()