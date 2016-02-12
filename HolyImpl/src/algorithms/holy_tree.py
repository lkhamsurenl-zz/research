from src.model.weight import Weight
from collections import deque
from src.model import grid
from src.view import draw_grid
from src.algorithms.initial_holy_tree import fast_initial_tree
from sets import Set

def update_weights(graph, source, pred, new_dist):
    """
    Given a source and new_dist with updated distance for source, propagate the distance through the graph.
    :param graph:
    :param source:
    :param new_dist:
    :return:
    """
    q = deque()
    q.appendleft(source)
    while len(q) != 0:
        u = q.pop()
        for v in u.neighbors.keys():
            if pred[v] != None and pred[v] == u:
                new_dist[v] = new_dist[u] + u.neighbors[v].weight
                q.appendleft(v)

def report(pred, dist):
    print("-------  Holy tree -------")
    for u in pred.keys():
        pu = pred[u] if pred[u] != None else "None"
        dpu = dist[pred[u]] if pred[u] != None and dist[pred[u]] != None else "None"
        du = dist[u] if dist[u] != None else "None"
        print("{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}".format(pu, u, dpu, du))
    print("------- --- -------")

def active_darts(s1, s2, pred):
    """
    Find all the active darts by labeling all the vertices:
    blue - decreasing in distance.
    red - increasing in distance.
    :param s1: current source
    :param s2: next source
    :param pred: current pred
    :param dist: current distance.
    :return: (blue, red) labeled sets
    """
    blue = Set([s2.name])
    # Construct all the blue vertices:
    for round in range(len(pred)):
        for v in pred:
            if pred[v] == None:
                continue
            if pred[v].name in blue:
                blue.add(v.name)
    red = set([v.name for v in pred.keys()]) - set(blue)
    return (set(blue), red)

def move_across_dart(graph, m, n, s1, s2, pred, dist):
    """
    Perform moving from s1 -> s2. Assume s1 and s2 are valid vertices in graph and connected by an edge.
    :param graph:
    :param s1: Source vertex.
    :param s2: Destination vertex.
    :return:
    """
    while pred[s1] != s2:
        # Get all the active darts.
        active = {}
        (blue, red) = active_darts(s1, s2, pred)
        #print("blue: {}; red: {}".format(blue, red))
        for u in graph.vertices:
            for v in u.neighbors:
                if u.name in blue and v.name in red:
                    active[u.neighbors[v]] = dist[u] + u.neighbors[v].weight - dist[v]

        #draw_grid.display(graph, m, n, s1.name, blue, red, pred)
        # Do pivot on dart with minimum slack.
        minimum_slack = Weight(length=float('inf'))
        min_dart = None
        for d in active.keys():
            if minimum_slack > active[d]:
                min_dart = d
                minimum_slack = active[d]

        if min_dart != None:
            draw_grid.display(graph, m, n, s1.name, blue, red, pred, min_dart)
            # Update dist and pred pointers respectively for the vertices.
            dist[min_dart.head] = dist[min_dart.tail] + min_dart.weight
            pred[min_dart.head] = min_dart.tail

            # DEBUG
            print("{} -> {} pivots in. {}".format(min_dart.tail, min_dart.head, min_dart.weight))
            #report(pred, dist)
            print("-------------------------------")

    # Done with the process, let's print out the new distances
    print("done with {0} -> {1}. New root is {1}".format(s1, s2))
    # s2's the new root.
    pred[s2] = None
    dist[s2] = Weight(homology=[0, 0])
    update_weights(graph, s2, pred, dist)
    #report(pred, dist)


def move_around_face(graph, m, n, vertices):
    """
    Move around the vertices in face in order, return all the SSSP for each vertex in vertices.
    :param graph: Graph to find MSSP
    :param vertices: face vertices given in order
    :return: All the shortest path distances for each vertex in the vertices list.
    """
    # Ensure there is at least one vertex when computing SSSP for each vertex in vertices.
    assert(len(vertices) > 1)
    s1 = vertices[0]  # first source vertex
    (pred, dist) = fast_initial_tree(graph, s1)
    (init_pred, init_dist) = (pred, dist)
    print("---Initial tree---")
    #report(pred, dist)
    print("----------------------")

    for i in range(len(vertices)):
        s1 = vertices[i]
        s2 = vertices[(i + 1) % len(vertices)]
        # Source will move from s1 -> s2, updating pred and dist dictionaries.
        move_across_dart(graph, m, n, s1, s2, pred, dist)

    # For sanity check, at the end of the cycle, dist and pred should be exactly same as the initial holy tree
    # computation.
    assert(init_dist == dist)
    assert(init_pred == pred)

def get_face_vertices(graph, names):
    vertices = []
    # Populate all the vertices given their names.
    for name in names:
        vertices.append(graph.get_vertex(name))
    return vertices

def main():
    """
    Main function to get all the MSSP distances as move around the face.
    :return:
    """
    m, n = 3, 3
    g1 = grid.g1()
    vertices = get_face_vertices(g1, [(1,1), (0,1), (0, 0), (1,0)])
    move_around_face(g1, m, n, vertices)

def debug():
    m, n = 3, 3
    g1 = grid.g1()
    vertices = get_face_vertices(g1, [(1,1), (0,1), (0, 0), (1,0)])
    move_around_face(g1, m, n, vertices)

def debug_grid():
    m, n = 3, 3
    g1 = grid.generate_2d_grid(m, n)
    vertices = get_face_vertices(g1, [(1,1), (0,1), (0, 0), (1,0)])
    move_around_face(g1, m, n, vertices)


debug_grid()
