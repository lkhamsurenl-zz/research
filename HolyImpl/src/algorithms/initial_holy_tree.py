from src.model.weight import Weight
from collections import deque

# TODO(lkhamsurenl): Measure performance of the fast_initial_tree.
def fast_initial_tree(graph, source):
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
            # NOTE(lkhamsurenl): Each vertex will be added only once to the queue.
            if v not in visited:
                queue.appendleft(v)
            # If tense, relax the dart.
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight
                pred[v] = u
    return (pred, dist)


def slow_initial_tree(graph, source):
    """
    :return: Predecessor pointer for initial holy tree.
    """
    pred = {source: None}
    dist = {}  # distance for each Vertex
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
        for v in u.neighbors.keys():
            # If tense, relax the dart.
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight
                pred[v] = u
                queue.appendleft(v)
    return (pred, dist)