import matplotlib.pyplot as plt
import networkx as nx
from sets import Set
from genus_boundary import resolve_boundary_darts, expand_vertices_list


def draw_primal(grid, root_name, blue, red, pred, vertex_mapping, pivot_dart=None, file=None):
    """
    Draw primal grid. Note that we replicate boundary vertices on visualization.
    :param grid: Grid graph to draw.
    :param root_name: Current root name. Used for annotating root vertex on visualization.
    :param blue: Vertices decreasing in distance.
    :param red: Vertices increasing in distance.
    :param pred: Predecessor pointer dictionary for current holy tree.
    :param vertex_mapping: Mapping of vertex to its boundary duplicates. {(i ,j) -> [(i, j), (a, b)], etc}
    :param pivot_dart: Current pivot dart.
    :param file: File to save the drawing.
    :return: Nothing
    """
    node_size = 400
    # Construct the width + 1 by height + 1 grid with directed edges.
    (G, pos) = __grid_layout__(grid.width, grid.height)

    # blue: distance decreasing
    blue_vertices = expand_vertices_list(blue, vertex_mapping)
    # red: distance increasing
    red_vertices = expand_vertices_list(red, vertex_mapping)

    blue_vertices, red_vertices = Set(blue_vertices), Set(red_vertices)
    if (-1,-1) in blue_vertices:
        blue_vertices.remove((-1, -1))
    if (-1,-1) in red_vertices:
        red_vertices.remove((-1, -1))

    # blue: both head and tail are blue
    # red: both head and tail are red
    # green: active darts with blue tail and red head.
    blue_darts, red_darts, green_darts = [], [], []
    for v in pred:
        u = pred[v]
        if u != None and u.name in blue_vertices and v.name in blue_vertices:
            blue_darts += resolve_boundary_darts(vertex_mapping[u.name], vertex_mapping[v.name])
        if u != None and u.name in red_vertices and v.name in red_vertices:
            red_darts += resolve_boundary_darts(vertex_mapping[u.name], vertex_mapping[v.name])

    for u in grid.vertices:
        for v in u.neighbors:
            if u.name >= (0,0) and v.name >= (0,0) and u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(vertex_mapping[u.name], vertex_mapping[v.name])

    # Draw darts with colored labels.
    nx.draw_spectral(G,edgelist=red_darts,width=3,alpha=1,edge_color='red')
    nx.draw_spectral(G,edgelist=blue_darts,width=3,alpha=1,edge_color='blue')
    nx.draw_spectral(G,edgelist=green_darts,width=4,alpha=1,edge_color='green')

    # Override label vertices with boundary.
    labels = __boundary_labels__(grid, vertex_mapping)
    nx.draw_networkx_labels(G, pos, labels=labels)

    # Label root with special text: "Root"
    nx.draw_spectral(G,node_size=node_size,nodelist=[root_name],labels={root_name:'\n\n\n Root'})

    # Use different color for pivot dart (Handle boundary duplication if necessary).
    pivot_dups = resolve_boundary_darts(vertex_mapping[pivot_dart.tail.name], vertex_mapping[pivot_dart.head.name]) if \
        pivot_dart is not None else []
    nx.draw_spectral(G,edgelist=pivot_dups,width=6,alpha=1,edge_color='black')
    # Annotate pivot dart label with "P".
    nx.draw_networkx_edge_labels(G, pos, edge_labels=__pivot_labels__(pivot_dups, "P"), label_pos=0.5)

    # Color vertices with labels.
    nx.draw_spectral(G,node_size=node_size,nodelist=blue_vertices,node_color='blue')
    nx.draw_spectral(G,node_size=node_size,nodelist=red_vertices,node_color='red')

    __draw_plot__(file)

def draw_dual(grid, root_name, blue, red, pred, face_mapping, pivot_dart=None, file=None):
    """
    Draw dual grid. Note that we replicate boundary faces on visualization.
    :param grid: Grid graph to draw.
    :param root_name: Current root name. Used for annotating root vertex on visualization.
    :param blue: Vertices decreasing in distance.
    :param red: Vertices increasing in distance.
    :param pred: Predecessor pointer dictionary for current holy tree.
    :param face_mapping: Mapping of faces to their boundary duplicates. {(i ,j) -> [(i, j), (a, b)], etc}
    :param pivot_dart: Current pivot dart.
    :param file: File to save the drawing.
    :return: Nothing
    """
    # Construct the width + 1 by height + 1 grid with directed edges.
    (G, pos) = __grid_layout__(grid.width, grid.height)

    # blue: distance decreasing
    blue_vertices = expand_vertices_list(blue, face_mapping)
    # red: distance increasing
    red_vertices = expand_vertices_list(red, face_mapping)

    blue_vertices, red_vertices = Set(blue_vertices), Set(red_vertices)
    if (-1,-1) in blue_vertices:
        blue_vertices.remove((-1, -1))
    if (-1,-1) in red_vertices:
        red_vertices.remove((-1, -1))

    core = Set() # keep track of all the edges in the 2-core in the dual.
    # blue: both head and tail are blue
    # red: both head and tail are red
    # green: active darts with blue tail and red head.
    blue_darts, red_darts, green_darts = [], [], []
    for u in grid.vertices:
        for v in u.neighbors:
            # u -> v in the primal Holy Tree, skip.
            if pred[v] == u or pred[u] == v:
                continue
            # u -> v is not in original graph (for instance, (-1, -1)), then skip.
            if u.name < (0,0) or v.name < (0,0):
                continue
            # u -> v has no dual defined, should not be the case.
            if u.neighbors[v].dual == None:
                print("No dual defined: {}".format(u.neighbors[v]))
                continue
            # Get the dual dart.
            dd = u.neighbors[v].dual
            core.add((min(dd.head.name, dd.tail.name), max(dd.head.name, dd.tail.name)))
            # If both u, v are blue, then dual dart is blue.
            if u.name in blue_vertices and v.name in blue_vertices:
                blue_darts += resolve_boundary_darts(face_mapping[dd.tail.name], face_mapping[dd.head.name])
            # If both u, v are red, then dual dart is blue.
            elif u.name in red_vertices and v.name in red_vertices:
                red_darts += resolve_boundary_darts(face_mapping[dd.tail.name], face_mapping[dd.head.name])
            # If both u blue, v is red, then dual dart is green.
            elif u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(face_mapping[dd.tail.name], face_mapping[dd.head.name])

    # Remove all hairs.
    done = False
    while not done:
        total_removed = 0
        for (t1, h1) in core:
            count_t1 = 1
            count_h1 = 1
            for (t2, h2) in core:
                if t1 == t2 and h1 == h2:
                    continue
                if t1 == t2 or t1 == h2:
                    count_t1 += 1
                if h1 == t2 or h1 == h2:
                    count_h1 += 1
            if count_t1 == 1 or count_h1 == 1:
                core.remove((t1, h1))
                total_removed += 1
                break
        if total_removed == 0:
            done = True

    # count how many time each vertex appear.
    count_vertex = {}
    for (t, h) in core:
        count_vertex[t] = count_vertex[t] + 1 if t in count_vertex else 1
        count_vertex[h] = count_vertex[h] + 1 if h in count_vertex else 1

    # Vertices appearing more than 2 are anchor vertices.
    anchor_vertices = []
    for v in count_vertex:
        if count_vertex[v] > 2:
            anchor_vertices.append(v)

    # Draw darts with colored labels.
    nx.draw_spectral(G,edgelist=red_darts,width=3,alpha=1,edge_color='red')
    nx.draw_spectral(G,edgelist=blue_darts,width=3,alpha=1,edge_color='blue')
    nx.draw_spectral(G,edgelist=green_darts,width=4,alpha=1,edge_color='green')

    # Override label vertices with boundary.
    labels = __boundary_labels__(grid, face_mapping, anchor_vertices)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    # Label root with special text: "Root". In dual graph, root is always (0, 0)
    # nx.draw_spectral(G,node_size=600,nodelist=[(0,0)],labels={(0, 0):'\n\n\n Root'})

    # Use different color for pivot dart (Handle boundary duplication if necessary).
    pivot_dups = resolve_boundary_darts(
        face_mapping[pivot_dart.dual.tail.name], face_mapping[pivot_dart.dual.head.name]) if \
        pivot_dart != None else []

    nx.draw_spectral(G,edgelist=pivot_dups,width=6,alpha=1,edge_color='black',node_color='white')
    # Label pivot dart with "P".
    nx.draw_networkx_edge_labels(G, pos, edge_labels=__pivot_labels__(pivot_dups, "P"), label_pos=0.5)

    __draw_plot__(file)

#####################                           HELPER  METHODS                            #############################

def __grid_layout__(width, height):
    # Construct the width + 1 by height + 1 grid with directed edges.
    G = nx.grid_2d_graph(width + 1, height + 1)
    G = nx.DiGraph(G)

    pos = nx.spectral_layout(G)

    return (G, pos)

def __boundary_labels__(grid, mapping, anchor_vertices={}):
    """
    Create labels for each vertex or face in grid, with resolved boundary. If (i, j) -> [(i, j), (a, b)], then
    both (i, j) and (a, b) should have label (i, j) in labels.
    :param grid:
    :param vertex_mapping:
    :return:
    """
    labels = {}
    for i in range(grid.width + 1):
        for j in range(grid.height + 1):
            for v in mapping:
                if (i, j) in mapping[v] and (i, j) in anchor_vertices:
                    labels[(i, j)] = u"\u2022{},{}\u2022".format(v[0], v[1])
                elif (i, j) in mapping[v]:
                    labels[(i, j)] = "{},{}".format(v[0], v[1])

    return labels

def __pivot_labels__(pivot_dups, label):
    """
    Create label for pivot dart in grid, with resolved boundary. If (i, j) -> [(i, j), (a, b)], then
    both (i, j) and (a, b) should have the label.
    :param pivot_dups: Duplicates of pivot with resolved boundary.
    :param label: Label to place for pivot.
    :return:
    """
    pivot_labels = {}
    for pivot in pivot_dups:
        pivot_labels[pivot] = label

    return pivot_labels

def __draw_plot__(file):
    """
    Either save plot to a file if given, otherwise draw on the screen. Note that user would have to close the drawing
    manually if drawn on the screen.
    :param file: File to save the plot.
    :return:
    """
    if file != None:
        plt.savefig(file, format='pdf')
        plt.close()
    else:
        plt.show()
