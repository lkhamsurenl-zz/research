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
    :return:
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
    G = nx.grid_2d_graph(m + 1, n + 1)
    G = nx.DiGraph(G)
    pos = nx.spectral_layout(G)

    # blue: distance decreasing
    # red: distance increasing
    blue_vertices, red_vertices = Set(blue), Set(red)
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
    for v in pred:
        u = pred[v]
        if u != None and u.name in blue_vertices and v.name in blue_vertices:
            blue_darts += resolve_boundary_darts(u.name, v.name, m, n)
        if u != None and u.name in red_vertices and v.name in red_vertices:
            red_darts += resolve_boundary_darts(u.name, v.name, m, n)

    for u in graph.vertices:
        for v in u.neighbors:
            if u.name in blue_vertices and v.name in red_vertices:
                green_darts += resolve_boundary_darts(u.name, v.name, m, n)

    # Draw darts with colored labels.
    nx.draw_spectral(G,edgelist=red_darts,width=3,alpha=1,edge_color='r')
    nx.draw_spectral(G,edgelist=blue_darts,width=3,alpha=1,edge_color='b')
    nx.draw_spectral(G,edgelist=green_darts,width=4,alpha=1,edge_color='g')

    # Color vertices with labels.
    nx.draw_spectral(G,node_size=600,nodelist=blue_vertices,node_color='b')
    nx.draw_spectral(G,node_size=600,nodelist=red_vertices,node_color='r')

    # Override label vertices with (m, j) -> (0, j) and (i, n) -> (i, 0)
    labels = {}
    for i in range(m + 1):
        for j in range(n + 1):
            labels[(i, j)] = (i % m, j % n)
    nx.draw_networkx_labels(G, pos, labels=labels)

        # Label root with special text: "Root"
    nx.draw_spectral(G,node_size=600,nodelist=[root_name],labels={root_name:'\n\n\n Root'})

    # Annotate pivot dart. Make duplicates for the pivot if it's boundary.
    # TODO(lkhamsurenl): Modify the color of pivoted vertex at the first time pivot.
    pivot_dups = resolve_boundary_darts(pivot_dart.tail.name, pivot_dart.head.name, m, n)
    edge_labels = {}
    for pivot in pivot_dups:
        edge_labels[pivot] = "Pivot"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    # Draw the graph on screen.
    plt.show()
