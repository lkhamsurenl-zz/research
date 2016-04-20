import copy
import datetime
import sys
from collections import deque
from sets import Set

from matplotlib.backends.backend_pdf import PdfPages

import src.model.edge
from src.algorithms.initial_holy_tree import fast_initial_tree
from src.model import grid
from src.model.dart import Dart
from src.model.weight import Weight
from src.view import draw_grid


def add_subtree(source, delta, pred, new_dist):
    """
    Given a source and new_dist with updated distance for source, propagate the distance through the graph.
    :param delta: Value to add to the subtree nodes.
    :param pred: predecessor pointers for current holy tree.
    :param source: Root of the subtree.
    :param new_dist: shortest path distance to each node.
    :return: Nothing.
    """
    new_dist[source] += delta
    q = deque()
    q.appendleft(source)
    while len(q) != 0:
        u = q.pop()
        for v in u.neighbors.keys():
            if pred[v] is not None and pred[v] == u:
                new_dist[v] = new_dist[u] + u.neighbors[v].weight
                q.appendleft(v)


def report(pred, dist):
    """
    :param pred: predecessor pointers for current holy tree.
    :param dist: distances in holy tree to each node from root.
    :return: Nothing.
    """
    # Report pred and dist for the holy tree.
    print(u"\u25bd\u25bd\u25bd Holy Tree \u25bd\u25bd\u25bd")
    for u in pred.keys():
        pu = pred[u] if pred[u] != None else "None"
        dpu = dist[pred[u]] if pred[u] != None and dist[pred[u]] != None else "None"
        du = dist[u] if dist[u] != None else "None"
        print("{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}".format(pu, u, dpu, du))
    print(u"\u25b3\u25b3\u25b3 Holy Tree \u25b3\u25b3\u25b3")


def report_multiple_distances(pred1, dist1, pred2, dist2):
    # Report the correct tree.
    print(u"\u25bd\u25bd\u25bd Correct Tree \u25bd\u25bd\u25bd")
    report(pred1, dist1)
    print(u"\u25b3\u25b3\u25b3 Correct Tree \u25b3\u25b3\u25b3")

    # Report the differing tree.
    print(u"\u25bd\u25bd\u25bd Output Tree \u25bd\u25bd\u25bd")
    report(pred2, dist2)
    print(u"\u25b3\u25b3\u25b3 Output Tree \u25b3\u25b3\u25b3")


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
    for i in range(len(pred)):
        for v in pred:
            if pred[v] is None:
                continue
            if pred[v].name in blue:
                blue.add(v.name)
    # All edges not in blue are red.
    red = set([v.name for v in pred.keys()]) - set(blue)
    return set(blue), red


def is_holy_tree(graph, g, pred, dist, title="is_holy_tree()"):
    """
    Check if there is no tense dart in graph.
    :param title: Example: Pivot (1, 2) -> (0, 2).
    :param graph:
    :param pred:
    :param dist:
    :return:
    """
    print(u"\u25bc\u25bc\u25bc {} \u25bc\u25bc\u25bc".format(title))
    for u in graph.vertices:
        for v in u.neighbors:
            slack = dist[u] + u.neighbors[v].weight - dist[v]
            if slack < Weight(homology=[0 for _ in range(2 * g)]) or \
                    (slack == Weight(homology=[0 for _ in range(2 * g)]) and pred[v] != u):
                print("is_holy_tree()={0}->{1} tense; dist[{0}]={2};dist[{1}]={3};weight={4};slack={5}".
                      format(u, v, dist[u], dist[v], u.neighbors[v].weight, slack))
    print(u"\u25b2\u25b2\u25b2 {} \u25b2\u25b2\u25b2".format(" " * len(title)))


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


def move_across_dart(graph, m, n, g, s1, s2, pred, dist, original_pdf=None, dual_pdf=None):
    """
    Perform moving from s1 -> s2. Assume s1 and s2 are valid vertices in graph and connected by an edge.
    :param m:
    :param n:
    :param dist:
    :param original_pdf: PDF file name to save the pivoting process.
    :param pred: predeccesor pointers defining current holy tree.
    :param dual_pdf: name of pdf file to save pivoting process.
    :param graph:
    :param s1: Source vertex.
    :param s2: Destination vertex.
    :return:
    """
    # Original value of the edge s1 -> s2.
    dart = copy.deepcopy(s1.neighbors[s2])
    # Distance from s to s1.
    lambda_weight = Weight(homology=[0 for _ in range(2 * g)])
    s = graph.add_vertex((-1, -1))  # special vertex to walk along the s1 -> s2.
    dist[s] = Weight(homology=[0 for _ in range(2 * g)])

    Dart(s, s1, Weight(0, [0 for _ in range(2 * g)], 0), dart.right, dart.left)
    Dart(s, s2, copy.deepcopy(dart.weight), dart.left, dart.right)

    remove_edge(s1, s2)  # Remove edge between s1, s2.
    pred[s] = None
    pred[s1] = s
    pred[s2] = s
    dist[s2] = s.neighbors[s2].weight

    # Reduce distance to both s1 and s2 form s by same value: Weight(0, -homology, -leafmost)
    Dart(s, s1, Weight(0, [-h for h in dart.weight.homology], -dart.weight.leafmost), dart.right, dart.left)
    add_subtree(s1, Weight(0, [-h for h in dart.weight.homology], -dart.weight.leafmost), pred, dist)

    Dart(s, s2, Weight(1, [0 for _ in range(2 * g)], 0), dart.left, dart.right)
    add_subtree(s2, Weight(0, [-h for h in dart.weight.homology], -dart.weight.leafmost), pred, dist)

    while True:
        # Get all the active darts.
        active = {}
        (blue, red) = active_darts(s1, s2, pred)
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
        if min_dart is not None and Weight(float(minimum_slack.length) / 2,
                                           [float(i) / 2 for i in minimum_slack.homology],
                                           float(minimum_slack.leafmost) / 2) + lambda_weight <= \
                Weight(1, [0 for _ in range(2 * g)], 0):
            draw_grid.display(graph, m, n, s1.name, blue, red, pred, min_dart, original_pdf)
            draw_grid.display_dual(graph, m, n, s1.name, blue, red, pred, min_dart, dual_pdf)

            # w represents the value to move s from s1 to s2.
            w = Weight(float(minimum_slack.length) / 2, [float(i) / 2 for i in minimum_slack.homology],
                       float(minimum_slack.leafmost) / 2)
            lambda_weight += w  # Keep track of the current progress.

            if pred[s1] == s:
                s.neighbors[s1].weight += w
                add_subtree(s1, w, pred, dist)

            if pred[s2] == s:
                s.neighbors[s2].weight -= w
                add_subtree(s2, -w, pred, dist)

            # Update dist and pred pointers respectively for the vertices.
            pred[min_dart.head] = min_dart.tail
            # here, if we check the values, it should still be the holy tree
            print("-------------------------------")
            is_holy_tree(graph, g, pred, dist, "Pivot: {}, slack: {}".format(min_dart, minimum_slack))

        else:  # no more pivot, move the values dart.weight - lambda_weight, then make the s2 new pivot
            draw_grid.display(graph, m, n, s1.name, blue, red, pred, None, original_pdf)
            draw_grid.display_dual(graph, m, n, s1.name, blue, red, pred, None, dual_pdf)
            delta = Weight(1, [0 for _ in range(2 * g)], 0) - lambda_weight
            add_subtree(s2, -delta, pred, dist)
            print("When moved all the way to {0}, distance to {0}: {1}".format(s2, dist[s2]))

            add_subtree(s1, delta, pred, dist)
            print(
                "When moved all the way to {0}, distance to {1}: {2}, dart: {3}".format(s2, s1, dist[s1], dart.weight))
            break

    graph.remove_vertex(s.name)
    del pred[s]
    del dist[s]
    # Insert back the edge between s1 and s2.
    src.model.edge.Edge(s1, s2, copy.deepcopy(dart.weight), dart.left, dart.right)

    # s2's the new root.
    pred[s2] = None
    pred[s1] = s2

    # Ensure that there is no tense dart at the end of the root move.
    is_holy_tree(graph, g, pred, dist, "Root {}".format(s2))

    # Compute actual holy tree @ s2, then compare it with the current tree.
    correct_pred, correct_dist = fast_initial_tree(graph, s2)
    assert correct_dist == dist, report_multiple_distances(correct_pred, correct_dist, pred, dist)
    assert correct_pred == pred, report_multiple_distances(correct_pred, correct_dist, pred, dist)

    print("done with {0} -> {1}. New root is {1}".format(s1, s2))


def move_around_face(graph, m, n, g, vertices):
    """
    Move around the vertices in face in order, return all the SSSP for each vertex in vertices.
    :param n: Height of the grid graph.
    :param m: Width of the grid graph.
    :param graph: Graph to find MSSP
    :param vertices: face vertices given in order
    :return: All the shortest path distances for each vertex in the vertices list.
    """
    # Ensure there is at least one vertex when computing SSSP for each vertex in vertices.
    assert (len(vertices) > 1)
    s1 = vertices[0]  # first source vertex
    (pred, dist) = fast_initial_tree(graph, s1)
    (init_pred, init_dist) = (pred, dist)

    print("---Initial tree---")
    report(pred, dist)
    is_holy_tree(graph, g, pred, dist, "Root {}".format(s1))
    print("----------------------")

    # Create a new pdf file with current timestamp.
    now = datetime.datetime.now()
    original_pdf = PdfPages('../../resources/{}-original.pdf'.format(now.strftime("%m-%d-%H:%M")))
    dual_pdf = PdfPages('../../resources/{}-dual.pdf'.format(now.strftime("%m-%d-%H:%M")))

    for i in range(len(vertices)):
        s1 = vertices[i]
        s2 = vertices[(i + 1) % len(vertices)]
        # Source will move from s1 -> s2, updating pred and dist dictionaries.
        move_across_dart(graph, m, n, g, s1, s2, pred, dist, original_pdf, dual_pdf)

    # Close the pdf file.
    if original_pdf is not None:
        original_pdf.close()
    if dual_pdf is not None:
        dual_pdf.close()

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
    g = 1
    g1 = grid.g1()
    vertices = get_face_vertices(g1, [(1, 1), (0, 1), (0, 0), (1, 0)])
    move_around_face(g1, m, n, g, vertices)


def debug_grid():
    m, n = 6, 6
    g = 1
    # Set deeper recursion level to avoid max recursion depth exceeded.
    if m > 5 or n > 5:
        sys.setrecursionlimit(10000)
    g1 = grid.generate_2d_grid(m, n)
    vertices = get_face_vertices(g1, [(1, 1), (0, 1), (0, 0), (1, 0)])
    move_around_face(g1, m, n, g, vertices)


debug_grid()
