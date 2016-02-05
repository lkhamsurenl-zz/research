__author__ = 'Luvsandondov Lkhamsuren'

class Vertex:
    '''
    Class Vertex, implemented with adjacency list method
    '''
    def __init__(self, name=None):
        self.name = name

        # Adjacency list contains the neighbor vertices.
        self.neighbors = {}

    def __str__(self):
        return self.name

    def get_neighbors(self):
        '''
        Get adjacency list for the vertex
        :return: Keys of all adjacent vertices
        '''
        return self.neighbors.keys()

    def add_dart(self, head, dart):
        '''
        add neighbor with given distance
        :param head: head of the dart
        :param dart: self is a tail of the dart.
        :return:
        '''
        self.neighbors[head] = dart

    # TODO(lkhamsurenl): Change this method to adding double arcs eventually.
    def add_edge(self, dest, weight):
        '''
        add neighbor with given distance
        :param destination_code: code name
        :param weight:  distance between
        :return:
        '''
        return NotImplemented

    def is_neighbor(self, vertex):
        '''
        Check if the given vertex_code is neighbor
        :param vertex
        :return: vertex
        '''
        return self.neighbors.get(vertex) != None

    def remove_dart(self, neighbor):
        '''
        # Given neighbor, remove the dart if exist:
        # NOTE: takes the destination code as an argument, not the name or actual vertex
        :param neighbor:
        :return:
        '''
        self.neighbors.pop(neighbor, None)

