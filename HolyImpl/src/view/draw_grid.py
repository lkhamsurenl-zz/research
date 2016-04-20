import matplotlib.pyplot as plt
import networkx as nx
from sets import Set
from genus_boundary import resolve_boundary_darts


def display(graph, m, n, root_name, blue, red, pred, vertex_mapping, pivot_dart=None, pp=None):
    node_size = 400
    # Construct the m + 1 by n + 1 grid with directed edges.
    G = nx.grid_2d_graph(m + 1, n + 1)
    G = nx.DiGraph(G)
    pos = nx.spectral_layout(G)

    # blue: distance decreasing
    blue_vertices = []
    for b in blue:
        if b in vertex_mapping:
            blue_vertices += vertex_mapping[b]
    # red: distance increasing
    red_vertices = []
    for r in red:
        if r in vertex_mapping:
            red_vertices += vertex_mapping[r]

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

    for u in graph.vertices:
        for v in u.neighbors:
            if u.name >= (0,0) and v.name >= (0,0) and u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(vertex_mapping[u.name], vertex_mapping[v.name])

    # Draw darts with colored labels.
    nx.draw_spectral(G,edgelist=red_darts,width=3,alpha=1,edge_color='red')
    nx.draw_spectral(G,edgelist=blue_darts,width=3,alpha=1,edge_color='blue')
    nx.draw_spectral(G,edgelist=green_darts,width=4,alpha=1,edge_color='green')

    # Override label vertices with (m, j) -> (0, j) and (i, n) -> (i, 0)
    labels = {}
    for i in range(m + 1):
        for j in range(n + 1):
            labels[(i, j)] = "{},{}".format(i % m, j % n)
    nx.draw_networkx_labels(G, pos, labels=labels)

    # Label root with special text: "Root"
    nx.draw_spectral(G,node_size=node_size,nodelist=[root_name],labels={root_name:'\n\n\n Root'})

    pivot_dups = resolve_boundary_darts(vertex_mapping[pivot_dart.tail.name], vertex_mapping[pivot_dart.head.name]) if \
        pivot_dart is not None else []
    nx.draw_spectral(G,edgelist=pivot_dups,width=6,alpha=1,edge_color='black')
    # Annotate pivot dart. Make duplicates for the pivot if it's boundary.
    edge_labels = {}
    for pivot in pivot_dups:
        edge_labels[pivot] = "P"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    # Color vertices with labels.
    nx.draw_spectral(G,node_size=node_size,nodelist=blue_vertices,node_color='blue')
    nx.draw_spectral(G,node_size=node_size,nodelist=red_vertices,node_color='red')

    # Save the pivoting process onto a file.
    if pp != None:
        plt.savefig(pp, format='pdf')
        plt.close()
    else:
        plt.show()

def display_dual(graph, m, n, root_name, blue, red, pred, vertex_mapping, pivot_dart=None, pp=None):
    # Construct the m + 1 by n + 1 grid with directed edges.
    G = nx.grid_2d_graph(m + 1, n + 1)
    # First let's not worry about the direction of the darts in the dual.
    G = nx.DiGraph(G)
    pos = nx.spectral_layout(G)

    # blue: distance decreasing
    blue_vertices = []
    for b in blue:
        if b in vertex_mapping:
            blue_vertices += vertex_mapping[b]
    # red: distance increasing
    red_vertices = []
    for r in red:
        if r in vertex_mapping:
            red_vertices += vertex_mapping[r]

    blue_vertices, red_vertices = Set(blue_vertices), Set(red_vertices)
    if (-1,-1) in blue_vertices:
        blue_vertices.remove((-1, -1))
    if (-1,-1) in red_vertices:
        red_vertices.remove((-1, -1))

    # blue: both head and tail are blue
    # red: both head and tail are red
    # green: active darts with blue tail and red head.
    blue_darts, red_darts, green_darts = [], [], []
    for u in graph.vertices:
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
            # If both u, v are blue, then dual dart is blue.
            if u.name in blue_vertices and v.name in blue_vertices:
                blue_darts += resolve_boundary_darts(vertex_mapping[dd.tail.name], vertex_mapping[dd.head.name])
            # If both u, v are red, then dual dart is blue.
            elif u.name in red_vertices and v.name in red_vertices:
                red_darts += resolve_boundary_darts(vertex_mapping[dd.tail.name], vertex_mapping[dd.head.name])
            # If both u blue, v is red, then dual dart is green.
            elif u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(vertex_mapping[dd.tail.name], vertex_mapping[dd.head.name])

    # Draw darts with colored labels.
    nx.draw_spectral(G,edgelist=red_darts,width=3,alpha=1,edge_color='red')
    nx.draw_spectral(G,edgelist=blue_darts,width=3,alpha=1,edge_color='blue')
    nx.draw_spectral(G,edgelist=green_darts,width=4,alpha=1,edge_color='green')

    # Override label vertices with (m, j) -> (0, j) and (i, n) -> (i, 0)
    labels = {}
    for i in range(m + 1):
        for j in range(n + 1):
            labels[(i, j)] = "{},{}".format(i % m, j % n)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    # Label root with special text: "Root". In dual graph, root is always (0, 0)
    # nx.draw_spectral(G,node_size=600,nodelist=[(0,0)],labels={(0, 0):'\n\n\n Root'})

    # Annotate pivot dart. Make duplicates for the pivot if it's boundary.
    # TODO(lkhamsurenl): Modify the color of pivoted vertex at the first time pivot.
    pivot_dups = resolve_boundary_darts(
        vertex_mapping[pivot_dart.dual.tail.name], vertex_mapping[pivot_dart.dual.head.name]) if \
        pivot_dart != None else []

    nx.draw_spectral(G,edgelist=pivot_dups,width=6,alpha=1,edge_color='black',node_color='white')
    # NOTE(lkhamsurenl): Label pivot with text label.
    edge_labels = {}
    for pivot in pivot_dups:
        edge_labels[pivot] = "P"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    # Save the pivoting process onto a file.
    if pp != None:
        plt.savefig(pp, format='pdf')
        plt.close()
    else:
        plt.show()
