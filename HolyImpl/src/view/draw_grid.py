import matplotlib.pyplot as plt
import networkx as nx
from sets import Set

def resolve_boundary_darts(u_name, v_name, m, n):
    """
    Boundary darts must be duplicated and resolved. For instance, (0, 0) -> (2, 0) must be resolved to
    { (3, 0) -> (2, 0), (2, 3) -> (3, 3) } when m = 3, n = 3
    :param u_name: Tail vertex name
    :param v_name: Head vertex name
    :param m: Width of the grid graph.
    :param n: Height of the grid graph.
    :return: All possible duplicates of (u_name -> v_name).
    """
    duplicates = []
    us, vs = Set([u_name]), Set([v_name])
    for i in [u_name[0], u_name[0] + m]:
        for j in [u_name[1], u_name[1] + n]:
            if i <= m and j <= n:
                us.add((i, j))
    for i in [v_name[0], v_name[0] + m]:
        for j in [v_name[1], v_name[1] + n]:
            if i <= m and j <= n:
                vs.add((i, j))
    for i in us:
        for j in vs:
            if abs(i[0] - j[0]) + abs(i[1] - j[1]) == 1:
                duplicates.append((i, j))
    return duplicates

def display(graph, m, n, root_name, blue, red, pred, pivot_dart):
    # Construct the m + 1 by n + 1 grid with directed edges.
    G = nx.grid_2d_graph(m + 1, n + 1)
    G = nx.DiGraph(G)
    pos = nx.spectral_layout(G)

    # blue: distance decreasing
    # red: distance increasing
    blue_vertices, red_vertices = Set(blue), Set(red)
    if (-1,-1) in blue_vertices:
        blue_vertices.remove((-1, -1))
    if (-1,-1) in red_vertices:
        red_vertices.remove((-1, -1))

    # Replicate color across horizontal boundary.
    # If (1, 0) is blue, then (m, 0) is also blue.
    for i in range(m + 1):
        if (i % m, 0) in blue:
            blue_vertices.add((i, n))
        elif (i % m, 0) in red:
            red_vertices.add((i, n))

    # Replicate color across horizontal boundary.
    # If (0, 1) is red, then (0, n) is also red.
    for j in range(n + 1):
        if (0, j % n) in blue:
            blue_vertices.add((m, j))
        elif (0, j % n) in red:
            red_vertices.add((m, j))

    # blue: both head and tail are blue
    # red: both head and tail are red
    # green: active darts with blue tail and red head.
    blue_darts, red_darts, green_darts = [], [], []
    for v in pred:
        u = pred[v]
        if u != None and u.name in blue_vertices and v.name in blue_vertices:
            blue_darts += resolve_boundary_darts(u.name, v.name, m, n)
        if u != None and u.name in red_vertices and v.name in red_vertices:
            red_darts += resolve_boundary_darts(u.name, v.name, m, n)

    for u in graph.vertices:
        for v in u.neighbors:
            if u.name >= (0,0) and v.name >= (0,0) and u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(u.name, v.name, m, n)

    # Draw darts with colored labels.
    nx.draw_spectral(G,edgelist=red_darts,width=3,alpha=1,edge_color='red')
    nx.draw_spectral(G,edgelist=blue_darts,width=3,alpha=1,edge_color='blue')
    nx.draw_spectral(G,edgelist=green_darts,width=4,alpha=1,edge_color='green')

    # Color vertices with labels.
    nx.draw_spectral(G,node_size=400,nodelist=blue_vertices,node_color='blue')
    nx.draw_spectral(G,node_size=400,nodelist=red_vertices,node_color='red')

    # Override label vertices with (m, j) -> (0, j) and (i, n) -> (i, 0)
    labels = {}
    for i in range(m + 1):
        for j in range(n + 1):
            labels[(i, j)] = "{},{}".format(i % m, j % n)
    nx.draw_networkx_labels(G, pos, labels=labels)

    # Label root with special text: "Root"
    nx.draw_spectral(G,node_size=400,nodelist=[root_name],labels={root_name:'\n\n\n Root'})


    pivot_dups = resolve_boundary_darts(pivot_dart.tail.name, pivot_dart.head.name, m, n)
    nx.draw_spectral(G,edgelist=pivot_dups,width=6,alpha=1,edge_color='black')
    # Annotate pivot dart. Make duplicates for the pivot if it's boundary.
    edge_labels = {}
    for pivot in pivot_dups:
        edge_labels[pivot] = "P"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    # Draw the graph on screen.
    plt.show()

def display_dual(graph, m, n, root_name, blue, red, pred, pivot_dart):
    # Construct the m + 1 by n + 1 grid with directed edges.
    G = nx.grid_2d_graph(m + 1, n + 1)
    # First let's not worry about the direction of the darts in the dual.
    # G = nx.DiGraph(G)
    pos = nx.spectral_layout(G)

    # blue: distance decreasing
    # red: distance increasing
    blue_vertices, red_vertices = Set(blue), Set(red)
    if (-1,-1) in blue_vertices:
        blue_vertices.remove((-1, -1))
    if (-1,-1) in red_vertices:
        red_vertices.remove((-1, -1))

    for i in range(m + 1):
        if (i % m, 0) in blue:
            blue_vertices.add((i, n))
        elif (i % m, 0) in red:
            red_vertices.add((i, n))

    for j in range(n + 1):
        if (0, j % n) in blue:
            blue_vertices.add((m, j))
        elif (0, j % n) in red:
            red_vertices.add((m, j))

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
                blue_darts += resolve_boundary_darts(dd.tail.name, dd.head.name, m, n)
            # If both u, v are red, then dual dart is blue.
            elif u.name in red_vertices and v.name in red_vertices:
                red_darts += resolve_boundary_darts(dd.tail.name, dd.head.name, m, n)
            # If both u blue, v is red, then dual dart is green.
            elif u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(dd.tail.name, dd.head.name, m, n)

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
    pivot_dups = resolve_boundary_darts(pivot_dart.dual.tail.name, pivot_dart.dual.head.name, m, n)

    nx.draw_spectral(G,edgelist=pivot_dups,width=6,alpha=1,edge_color='black',node_color='white')
    # NOTE(lkhamsurenl): Label pivot with text label.
    edge_labels = {}
    for pivot in pivot_dups:
        edge_labels[pivot] = "P"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    # Draw the graph on screen.
    plt.show()