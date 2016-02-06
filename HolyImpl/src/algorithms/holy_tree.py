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

    queue = deque()
    queue.appendleft(source)
    while len(queue) != 0:
        u = queue.pop()
        visited[u] = 1
        for v in u.neighbors.keys():
            if v not in visited:
                queue.appendleft(v)
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight

                pred[v] = u

    return (pred, dist)

g1 = G1()
s = g1.get_vertex("h")
(pred, dist) = initial_tree(g1, s)
for u in pred.keys():
    pu = pred[u] if pred[u] != None else "None"
    dpu = dist[pred[u]] if pred[u] != None and dist[pred[u]] != None else "None"
    du = dist[u] if dist[u] != None else "None"
    print("{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}".format(pu, u, dpu, du))