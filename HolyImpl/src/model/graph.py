from src.model.vertex import Vertex

__author__ = 'Luvsandondov Lkhamsuren'

class Graph:

    def __init__(self, vertices=[], faces=[], genus=0):
        # vertices of the graph.
        self.vertices = vertices
        # faces of the graph (corresponding to the vertices in the dual graph).
        self.faces = faces
        # Graph's genus. For planar embedded graphs, g = 0.
        assert genus < 3, "We only support g < 3 options for now."
        self.genus = genus

    # TODO(lkhamsurenl): Remove vertex should get rid of all the edges too.
    def remove_vertex(self, vertex_name):
        vertex = None
        for v in self.vertices:
            if v.name == vertex_name:
                vertex = v
        # Remove darts.
        for v in self.vertices:
            if vertex in v.neighbors:
                del v.neighbors[vertex]
        # Remove the vertex from the list of vertices in the graph.
        self.vertices.remove(vertex)
        return vertex

    def add_vertex(self, vertex_name):
        v = Vertex(vertex_name)
        self.vertices.append(v)
        return v

    def get_vertex(self, vertex_name):
        for v in self.vertices:
            if v.name == vertex_name:
                return v
        return None

    def get_vertices(self, vertices_names):
        vs = []
        # Populate all the vertices given their names.
        for name in vertices_names:
            vs.append(self.get_vertex(name))
        return vs

    def get_face(self, face_name):
        for f in self.faces:
            if f.name == face_name:
                return f
        return None


    def get_genus(self):
        return self.genus

    def pretty_print(self):
        print("--- Vertices ---")
        for u in self.vertices:
            for v in u.neighbors:
                print(u.neighbors[v])
        print("--- Faces ---")
        for f in self.faces:
            for g in f.neighbors:
                print(f.neighbors[g])