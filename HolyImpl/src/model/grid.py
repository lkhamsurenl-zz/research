import copy

from src.model.edge import Edge
from src.model.graph import Graph
from src.model.vertex import Vertex
from src.model.weight import Weight
from src.algorithms.traversal import bfs


def remove_edge(u, v):
    du = u.neighbors[v].dual.head
    dv = u.neighbors[v].dual.tail

    u.remove_dart(v)
    v.remove_dart(u)
    du.remove_dart(dv)
    dv.remove_dart(du)

def compute_leafmost(spanning_tree):
    """
    Return learfmost term for each edge in following format:
    (source_name, destination_name): leafmost_term
    :param spanning_tree: dict of {src_name: dst_name}
    :return:
    """
    leafmost = {}
    num_children = {}
    for v_name in spanning_tree.keys():
        num_children[v_name] = 0
    while len(spanning_tree) != 0:
        count = {}
        for v_name in spanning_tree.keys():
            u_name = spanning_tree[v_name]
            count[v_name] = count[v_name] + 1 if v_name in count else 1
            count[u_name] = count[u_name] + 1 if u_name in count else 1
        # Find which ones are the leaf
        for v_name in count.keys():
            if count[v_name] == 1 and v_name != None:
                # TODO(lkhamsurenl): Current leafmost assignment points away from the root face. Negating would
                # reverse the direction.
                leafmost[(spanning_tree[v_name], v_name)] = num_children[v_name] + 1
                num_children[spanning_tree[v_name]] = num_children[spanning_tree[v_name]] + num_children[v_name] + 1 \
                    if spanning_tree[v_name] != None else 0
                del spanning_tree[v_name]

    return leafmost

def print_spanning_tree(pred):
    print("-------------------")
    for v in pred:
        print("{} -> {}".format(pred[v], v))
    print("-------------------")

def grid(m, n):
    """
    Create m x n grid graph with genus 1.
    1st row and last column are the homology cycles.
    Bottom left face is the MSSP face with top right vertex of this face being the first source.
    :param m:
    :param n:
    :return:
    """
    # Generate vertices and faces.
    vs, fs = [[None for j in range(n)] for i in range(m)], [[None for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            vs[i][j] = Vertex((i, j))
            fs[i][j] = Vertex((i, j))

    # Generate all edges and its duals.
    for i in range(m):
        for j in range(n):
            v = vs[i][j]
            # Dart (i, j) -> (i + 1, j), its reverse, dual, dual reverse.
            neighbor = vs[(i + 1) % m][j]  # Compute left and right face coordinates.
            left = fs[i][j]
            right = fs[i][(j - 1) % n]

            if i == m - 1:
                Edge(v, neighbor, Weight(1, [0, -1], 0), left, right)
            else:
                Edge(v, neighbor, Weight(1, [0, 0], 0), left, right)

            # Dart (i, j) -> (i, j + 1), its reverse, dual, dual reverse.
            neighbor = vs[i][(j + 1) % n]  # Compute left and right face coordinates.
            left = fs[(i - 1) % m][j]
            right = fs[i][j]

            if j == n - 1:
                Edge(v, neighbor, Weight(1, [1, 0], 0), left, right)
            else:
                Edge(v, neighbor, Weight(1, [0, 0], 0), left, right)

    graph = Graph(vertices=sum(vs, []), faces=sum(fs, []))

    # Num Edge(spanning tree) + Num edges(dual spanning tree) + 2 * g
    # Spanning tree in original graph. Note that we first remove non-trivial homology edges from graph prior to
    # computing spanning tree.
    # TODO(lkhamsurenl): Figure out a way to find Spanning tree without explicit copy of the entire graph.
    c_st = copy.deepcopy(graph)
    for i in range(m):
        c_u = c_st.get_vertex((i, n-1))
        c_v = c_st.get_vertex((i,0))
        remove_edge(c_u, c_v)
    for j in range(n):
        c_u = c_st.get_vertex((m-1, j))
        c_v = c_st.get_vertex((0,j))
        remove_edge(c_u, c_v)

    spanning_tree = bfs(c_st.get_vertex((1,1)))
    # print_spanning_tree(spanning_tree)

    # Dual spanning tree. Note that we remove all edges in spanning tree and 2g auxiliary edges (which in our case:
    # (0,n-1) -> (0,0) and (m-1, 0) -> (0,0)).
    c_g = copy.deepcopy(graph)
    for v_name in spanning_tree:
        u_name = spanning_tree[v_name]
        if u_name != None:
            remove_edge(c_g.get_vertex(u_name), c_g.get_vertex(v_name))
    remove_edge(c_g.get_vertex((0,n-1)), c_g.get_vertex((0,0)))
    remove_edge(c_g.get_vertex((m-1,0)), c_g.get_vertex((0,0)))

    dual_spanning_tree = bfs(c_g.get_face((0,0)))
    # print_spanning_tree(dual_spanning_tree)

    leafmost = compute_leafmost(dual_spanning_tree)
    for (u_name, v_name) in leafmost:
        if u_name != None:
            u = graph.get_face(u_name)
            v = graph.get_face(v_name)

            dart = u.neighbors[v]
            dart.weight = Weight(dart.weight.length, dart.weight.homology, leafmost[(u_name, v_name)])
            # Create reverse, dual, dual reverse respectively with corresponding leafmost terms.
            dart.create_reverse_dart()
            dual_dart = dart.create_dual_dart()
            dual_dart.create_reverse_dart()

    return graph
