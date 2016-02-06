from src.model.dart import Dart
from src.model.vertex import Vertex
from src.model.weight import Weight
from collections import deque
from src.model.g1 import G1


def initial_tree(graph, source):
    """
    :return: Predecessor pointer for initial holy tree.
    """
    pred = {source: None}
    dist = {}  # distance for each Vertex
    visited = {}  # keep track of which vertices we visited.
    # Initialize the distance values.
    dist[source] = Weight(homology=[0, 0])
    for v in graph.vertices:
        if v != source:
            dist[v] = Weight(length=float('inf'))
    # queue dictates which order we visit vertices.
    queue = deque()
    queue.appendleft(source)
    while len(queue) != 0:
        u = queue.pop()
        visited[u] = 1
        for v in u.neighbors.keys():
            # Add to the queue if has not been visited.
            if v not in visited:
                queue.appendleft(v)
            # If tense, relax the dart.
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight
                pred[v] = u
    return (pred, dist)


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
            #print("{0} -> {1}; pred[{1}] = {2}".format(u, v, pred[v]))
            if pred[v] != None and pred[v] == u:
                new_dist[v] = new_dist[u] + u.neighbors[v].weight
                q.appendleft(v)


def move_around_face():
    g1 = G1()
    s = g1.get_vertex("h")
    (pred, dist) = initial_tree(g1, s)
    for u in pred.keys():
        pu = pred[u] if pred[u] != None else "None"
        dpu = dist[pred[u]] if pred[u] != None and dist[pred[u]] != None else "None"
        du = dist[u] if dist[u] != None else "None"
        #print("{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}".format(pu, u, dpu, du))
    # Do the first moving around the face part:
    # h -> d
    print("starting h -> d")
    lambd = 0
    while lambd != 1:
        new_dist = {}
        #s = Vertex("s")  # new vertex initially sitting on h then to d
        h = g1.get_vertex("h")
        #dart = Dart(s, h, Weight(0, [0, 0], 0))
        #dart.create_reverse_dart()

        d = g1.get_vertex("d")
        #dart = Dart(d, h, Weight(1, [0, 0], 0))
        #dart.create_reverse_dart()

        lambd += 0.1
        # Find vertices with slack decreasing
        new_dist[h] = Weight(lambd, dist[h].homology, dist[h].leafmost)
        update_weights(g1, h, pred, new_dist)

        new_dist[d] = Weight(1 - lambd, dist[d].homology, dist[d].leafmost)
        update_weights(g1, d, pred, new_dist)
        for u in new_dist:
            print("new_dist({}) = {}; dist = {}".format(u, new_dist[u], dist[u]))


        # For each edges, relax if necessary
        for u in g1.vertices:
            for v in u.neighbors.keys():
                # If tense, relax the dart.
                if new_dist[u] + u.neighbors[v].weight < new_dist[v]:
                    new_dist[v] = new_dist[u] + u.neighbors[v].weight
                    print("{} -> {} pivots in.".format(u, v))
                    pred[v] = u

        dist = new_dist

move_around_face()
