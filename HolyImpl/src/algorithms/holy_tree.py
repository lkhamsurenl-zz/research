import copy
from sets import Set

from matplotlib.backends.backend_pdf import PdfPages

import src.model.edge
from src.algorithms.initial_holy_tree import fast_initial_tree
from src.model.dart import Dart
from src.model.grid import Grid
from src.model.weight import Weight
from src.view.draw_grid import draw_dual, draw_primal

def move_across_dart(grid, s1, s2, holy_tree, visual_params):
    """
    Move across dart s1 -> s2, changing holy_tree through series of pivots.
    :param grid:
    :param holy_tree: Holy tree rooted at s1.
    :param s1: Source vertex.
    :param s2: Destination vertex.
    :param visual_params: (vertex_mapping, face_mapping, primal_pdf, dual_pdf).
    :return:
    """
    # Original value of the edge s1 -> s2.
    dart = copy.deepcopy(s1.neighbors[s2])
    # Distance from s to s1.
    lambda_weight = Weight(homology=[0 for _ in range(2 * grid.genus)])
    s = grid.add_vertex((-1, -1))  # special vertex to walk along the s1 -> s2.
    holy_tree.dist[s] = Weight(homology=[0 for _ in range(2 * grid.genus)])

    Dart(s, s1, Weight(0, [0 for _ in range(2 * grid.genus)], 0), dart.right, dart.left)
    Dart(s, s2, copy.deepcopy(dart.weight), dart.left, dart.right)

    # Remove edge between s1, s2.
    __remove_edge__(s1, s2)

    # Fix pred pointers.
    holy_tree.pred[s] = None
    holy_tree.pred[s1] = s
    holy_tree.pred[s2] = s

    # Set dist to s2.
    holy_tree.dist[s2] = s.neighbors[s2].weight

    # Reduce distance to both s1 and s2 form s by same value: Weight(0, -homology, -leafmost)
    Dart(s, s1, Weight(0, [-h for h in dart.weight.homology], -dart.weight.leafmost), dart.right, dart.left)
    holy_tree.add_subtree(s1, Weight(0, [-h for h in dart.weight.homology], -dart.weight.leafmost))

    Dart(s, s2, Weight(1, [0 for _ in range(2 * grid.genus)], 0), dart.left, dart.right)
    holy_tree.add_subtree(s2, Weight(0, [-h for h in dart.weight.homology], -dart.weight.leafmost))

    while True:
        # Get all the active darts.
        active = {}
        (blue, red) = __active_darts__(s1, s2, holy_tree.pred)
        for u in grid.vertices:
            for v in u.neighbors:
                if u.name in blue and v.name in red:
                    active[u.neighbors[v]] = holy_tree.dist[u] + u.neighbors[v].weight - holy_tree.dist[v]

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
                Weight(1, [0 for _ in range(2 * grid.genus)], 0):
            draw_primal(grid, (s1.name,s2.name), blue, red, holy_tree.pred, visual_params[0], min_dart, visual_params[2])
            draw_dual(grid, blue, red, holy_tree.pred, visual_params[1], min_dart, visual_params[3])

            # w represents the value to move s from s1 to s2.
            w = Weight(float(minimum_slack.length) / 2, [float(i) / 2 for i in minimum_slack.homology],
                       float(minimum_slack.leafmost) / 2)
            lambda_weight += w  # Keep track of the current progress.

            if holy_tree.pred[s1] == s:
                s.neighbors[s1].weight += w
                holy_tree.add_subtree(s1, w)

            if holy_tree.pred[s2] == s:
                s.neighbors[s2].weight -= w
                holy_tree.add_subtree(s2, -w)

            # Update dist and pred pointers respectively for the vertices.
            holy_tree.pred[min_dart.head] = min_dart.tail
            # here, if we check the values, it should still be the holy tree
            print("-------------------------------")
            print(holy_tree.is_holy_tree(grid, "Pivot: {}, slack: {}".format(min_dart, minimum_slack)))

        else: # no more pivot, move the values dart.weight - lambda_weight, then make the s2 new pivot
            draw_primal(grid, (s1.name,s2.name), blue, red, holy_tree.pred, visual_params[0], None, visual_params[2])
            draw_dual(grid, blue, red, holy_tree.pred, visual_params[1], None, visual_params[3])

            delta = Weight(1, [0 for _ in range(2 * grid.genus)], 0) - lambda_weight
            holy_tree.add_subtree(s2, -delta)
            print("When moved all the way to {0}, distance to {0}: {1}".format(s2, holy_tree.dist[s2]))

            holy_tree.add_subtree(s1, delta)
            print("When moved all the way to {0}, distance to {1}: {2}, dart: {3}".format(s2, s1, holy_tree.dist[s1],
                                                                                        dart.weight))
            break

    # Remove s.
    grid.remove_vertex(s.name)
    del holy_tree.pred[s]
    del holy_tree.dist[s]

    # Insert back the edge between s1 and s2.
    src.model.edge.Edge(s1, s2, copy.deepcopy(dart.weight), dart.left, dart.right)

    # s2 is the new root.
    holy_tree.pred[s2] = None
    holy_tree.pred[s1] = s2

    # Ensure that there is no tense dart at the end of the root move.
    print(holy_tree.is_holy_tree(grid, "Root {}".format(s2)))

    # Compute correct holy tree rooted at s2, ensure it is equal to the current holy tree.
    correct_holy_tree = fast_initial_tree(grid, grid.genus, s2)
    assert correct_holy_tree == holy_tree, holy_tree.report_difference(correct_holy_tree)

    print("done with {0} -> {1}. New root is {1}".format(s1, s2))


def move_around_face(grid, vertices, visual_params):
    """
    Move around the vertices of the given face in order, by continuously moving across darts connecting consecutive
    vertices.
    :param grid: Grid graph to compute MSSP
    :param vertices: face vertices given in order
    :return: All the shortest path distances for each vertex in the vertices list.
    """
    # Ensure there is at least one vertex when computing SSSP for each vertex in vertices.
    assert (len(vertices) > 1)
    s1 = vertices[0]  # first source vertex
    holy_tree = fast_initial_tree(grid, grid.genus, s1)

    print("---Initial tree---\n{}".format(holy_tree))
    print(holy_tree.is_holy_tree(grid, "Root {}".format(s1)))
    print("----------------------")

    for i in range(len(vertices)):
        s1 = vertices[i]
        s2 = vertices[(i + 1) % len(vertices)]
        # Source will move from s1 -> s2, updating pred and dist dictionaries.
        move_across_dart(grid, s1, s2, holy_tree, visual_params)

    # For sanity check, at the end of the cycle, holy tree should be exactly same as the initial holy tree.
    initial_holy_tree = fast_initial_tree(grid, grid.genus, vertices[0])
    assert initial_holy_tree == holy_tree, holy_tree.report_difference(initial_holy_tree)

#####################                           HELPER  METHODS                            #############################

def __active_darts__(s1, s2, pred):
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

def __remove_edge__(u, v):
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
