from src.model.vertex import Vertex

__author__ = 'Luvsandondov Lkhamsuren'

class Graph:

    def __init__(self, vertices=[], faces=[]):
        self.vertices = vertices
        self.faces = faces

    # TODO(lkhamsurenl): Remove vertex should get rid of all the edges too.
    def remove_vertex(self, vertex_name):
        vertex = None
        for v in self.vertices:
            if v.name == vertex_name:
                vertex = v
                self.vertices.remove(vertex)
                break
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

    def get_face(self, face_name):
        for f in self.faces:
            if f.name == face_name:
                return f
        return None