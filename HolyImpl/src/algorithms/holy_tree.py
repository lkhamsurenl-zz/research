import copy
import sys

from src.model.dart import Dart
from src.model.edge import Edge
from src.model.vertex import Vertex
from src.model.weight import Weight
from collections import deque
from src.model import grid
from src.view import draw_grid
from src.algorithms.initial_holy_tree import fast_initial_tree
from sets import Set


def add_subtree(source, delta, pred, new_dist):
    """
    Given a source and new_dist with updated distance for source, propagate the distance through the graph.
    :param graph:
    :param source:
    :param new_dist:
    :return: Nothing.
    """
    new_dist[source] += delta
    q = deque()
    q.appendleft(source)
    while len(q) != 0:
        u = q.pop()
        for v in u.neighbors.keys():
            if pred[v] != None and pred[v] == u:
                new_dist[v] = new_dist[u] + u.neighbors[v].weight
                q.appendleft(v)


def report(pred, dist):
    # Report pred and dist for the holy tree.
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
    :param pred: predecessor pointers construct the SSSP rooted at s1.
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
    # All edges not in blue are red.
    red = set([v.name for v in pred.keys()]) - set(blue)
    return (set(blue), red)


def is_holy_tree(graph, pred, dist):
    """
    Check if there is no tense dart in graph.
    :param graph:
    :param pred:
    :param dist:
    :return:
    """
    is_holy = True
    for u in graph.vertices:
        for v in u.neighbors:
            slack = dist[u] + u.neighbors[v].weight - dist[v]
            if slack < Weight(homology=[0, 0]) or (slack == Weight(homology=[0, 0]) and pred[v] != u):
                print("is_holy_tree() = {0} -> {1} is tense.dist[{0}]={2}, dist[{1}] = {3}, weight = {4}; slack = {5}".
                      format(u, v, dist[u], dist[v], u.neighbors[v].weight, slack))
                is_holy = False
    return is_holy

def remove_edge(u, v):
    """
    Remove all the edges in u <-> v.
    :param u:
    :param v:
    :return: nothing
    """
    # du = u.neighbors[v].dual.head
    # dv = u.neighbors[v].dual.tail

    u.remove_dart(v)
    v.remove_dart(u)
    # du.remove_dart(dv)
    # dv.remove_dart(du)

def move_across_dart(graph, m, n, s1, s2, pred, dist, acc):
    """
    Perform moving from s1 -> s2. Assume s1 and s2 are valid vertices in graph and connected by an edge.
    :param graph:
    :param s1: Source vertex.
    :param s2: Destination vertex.
    :return:
    """
    dart = copy.deepcopy(s1.neighbors[s2])

    lambda_weight = Weight(homology=[0,0])
    s = graph.add_vertex((-1,-1)) # special vertex to walk along the s1 -> s2.
    dist[s] = Weight(homology=[0,0])

    Dart(s, s1, Weight(0,[-2*h for h in s1.neighbors[s2].weight.homology], -2 * s1.neighbors[s2].weight.leafmost),\
         s1.neighbors[s2].right, s1.neighbors[s2].left)

    Dart(s, s2, copy.deepcopy(s1.neighbors[s2].weight), s1.neighbors[s2].left, s1.neighbors[s2].right)

    remove_edge(s1, s2) # Remove edge btw s1, s2.
    pred[s] = None
    pred[s1] = s
    add_subtree(s1, s.neighbors[s1].weight, pred, dist)

    pred[s2] = s
    dist[s2] = s.neighbors[s2].weight

    while True:
        # Get all the active darts.
        active = {}
        (blue, red) = active_darts(s1, s2, pred)
        # print("blue: {}; red: {}".format(blue, red))
        for u in graph.vertices:
            for v in u.neighbors:
                if u.name in blue and v.name in red:
                    active[u.neighbors[v]] = dist[u] + u.neighbors[v].weight - dist[v]

        # Do pivot on dart with minimum slack.
        minimum_slack = Weight(length=float('inf'))
        min_dart = None
        for d in active.keys():
            if minimum_slack > active[d]:
                min_dart = d
                minimum_slack = active[d]

        # Check the value of the min_slack / 2 would not result in s "go over" s2.
        if min_dart != None and Weight(float(minimum_slack.length) / 2, [float(i) / 2 for i in minimum_slack.homology],\
                       float(minimum_slack.leafmost) / 2) + lambda_weight < dart.weight:
            draw_grid.display(graph, m, n, s1.name, blue, red, pred, min_dart)

            # DEBUG
            print("{} -> {} pivots in. {}. {}".format(min_dart.tail, min_dart.head, min_dart.weight, minimum_slack))
            acc[(min_dart.tail.name, min_dart.head.name)] = acc[(min_dart.tail.name, min_dart.head.name)] + 1 \
                if (min_dart.tail.name, min_dart.head.name) in acc else 1
            # report(pred, dist)
            print("-------------------------------")

            # w represents the value to move s from s1 to s2.
            w = Weight(float(minimum_slack.length) / 2, [float(i) / 2 for i in minimum_slack.homology],\
                       float(minimum_slack.leafmost) / 2)
            lambda_weight += w # Keep track of the current progress.

            if pred[s1] == s:
                s.neighbors[s1].weight += w
                add_subtree(s1, w, pred, dist)

            if pred[s2] == s:
                s.neighbors[s2].weight -= w
                add_subtree(s2, -w, pred, dist)

            # Update dist and pred pointers respectively for the vertices.
            #dist[min_dart.head] = dist[min_dart.tail] + min_dart.weight
            pred[min_dart.head] = min_dart.tail
            # here, if we check the values, it should still be the holy tree
            print("Check after pivot {} -> {}: {}".format(min_dart.tail, min_dart.head, is_holy_tree(graph, pred, dist)))

        else: # no more pivot, move the values dart.weight - lambd, then make the s2 new pivot
            delta = dart.weight - lambda_weight
            add_subtree(s2, -delta, pred, dist)
            print("When moved all the way to {0}, distance to {0}: {1}".format(s2, dist[s2]))

            add_subtree(s1, delta, pred, dist)
            print("When moved all the way to {0}, distance to {1}: {2}, dart: {3}".format(s2, s1, dist[s1], dart.weight))
            break

    # Done with the process, let's print out the new distances
    print("done with {0} -> {1}. New root is {1}".format(s1, s2))

    graph.remove_vertex(s.name)
    del pred[s]
    del dist[s]
    Edge(s1, s2, copy.deepcopy(dart.weight), dart.left, dart.right)

    # s2's the new root.
    pred[s2] = None
    pred[s1] = s2

    # Ensure that there is no tense dart at the end of the root move.
    print("no tense dart at root {}: {}".format(s2, is_holy_tree(graph, pred, dist)))

    # Compute actual holy tree @ s2, then compare
    correct_pred, correct_dist = fast_initial_tree(graph, s2)
    assert correct_dist == dist
    assert correct_pred == pred
    #report(correct_pred, correct_dist)
    #report(pred, dist)
    print("--- done with current root ---")

def move_around_face(graph, m, n, vertices):
    """
    Move around the vertices in face in order, return all the SSSP for each vertex in vertices.
    :param graph: Graph to find MSSP
    :param vertices: face vertices given in order
    :return: All the shortest path distances for each vertex in the vertices list.
    """
    # Ensure there is at least one vertex when computing SSSP for each vertex in vertices.
    assert (len(vertices) > 1)
    s1 = vertices[0]  # first source vertex
    (pred, dist) = fast_initial_tree(graph, s1)
    (init_pred, init_dist) = (pred, dist)
    acc = {}
    for v in pred:
        u = pred[v]
        if u != None:
            acc[(u.name, v.name)] = 1
    print("---Initial tree---")
    report(pred, dist)
    print("initial tree holy: {}".format(is_holy_tree(graph, pred, dist)))
    print("----------------------")

    for i in range(len(vertices)):
        s1 = vertices[i]
        s2 = vertices[(i + 1) % len(vertices)]
        # Source will move from s1 -> s2, updating pred and dist dictionaries.
        move_across_dart(graph, m, n, s1, s2, pred, dist, acc)

    print("Pivot summary: \n {}".format(acc))

    # For sanity check, at the end of the cycle, dist and pred should be exactly same as the initial holy tree
    # computation.
    assert (init_dist == dist)
    assert (init_pred == pred)


def get_face_vertices(graph, names):
    vertices = []
    # Populate all the vertices given their names.
    for name in names:
        vertices.append(graph.get_vertex(name))
    return vertices

def debug():
    m, n = 3, 3
    g1 = grid.g1()
    vertices = get_face_vertices(g1, [(1, 1), (0, 1), (0, 0), (1, 0)])
    move_around_face(g1, m, n, vertices)

def debug_grid():
    sys.setrecursionlimit(10000)
    m, n = 4, 4
    g1 = grid.generate_2d_grid(m, n)
    vertices = get_face_vertices(g1, [(1, 1), (0, 1), (0, 0), (1, 0)])
    move_around_face(g1, m, n, vertices)

debug_grid()
