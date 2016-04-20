import copy

from src.model.edge import Edge
from src.model.graph import Graph
from src.model.vertex import Vertex
from src.model.weight import Weight
from src.algorithms.traversal import bfs

__author__ = 'Luvsandondov Lkhamsuren'

def remove_edge(u, v):
    """
    Remove all the edges in u <-> v.
    :param u: tail vertex.
    :param v: head vertex.
    :return: nothing
    """
    du = u.neighbors[v].dual.head
    dv = u.neighbors[v].dual.tail

    u.remove_dart(v)
    v.remove_dart(u)
    du.remove_dart(dv)
    dv.remove_dart(du)

def print_spanning_tree(pred):
    print("-------------------")
    for v in pred:
        print("{} -> {}".format(pred[v], v))
    print("-------------------")

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
                # TODO(lkhamsurenl): Current leafmost assignment points away from the root face.
                # NOTE(lkhamsurenl): Negating would reverse the direction.
                leafmost[(spanning_tree[v_name], v_name)] = num_children[v_name] + 1
                num_children[spanning_tree[v_name]] = num_children[spanning_tree[v_name]] + num_children[v_name] + 1 \
                    if spanning_tree[v_name] != None else 0
                del spanning_tree[v_name]

    return leafmost

def generate_2d_grid(m, n):
    """
    Create m x n grid graph with genus 1.
    1st row and last column are the homology cycles.
    Bottom left face is the MSSP face with top right vertex of this face being the first source.
    :param m:
    :param n:
    :return:
    """
    # Generate vertices and faces.
    vs = [[Vertex((i, j)) for j in range(n)] for i in range(m)]
    fs = [[Vertex((i, j)) for j in range(n)] for i in range(m)]

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
        c_u = c_st.get_vertex((i, n - 1))
        c_v = c_st.get_vertex((i, 0))
        remove_edge(c_u, c_v)
    for j in range(n):
        c_u = c_st.get_vertex((m - 1, j))
        c_v = c_st.get_vertex((0, j))
        remove_edge(c_u, c_v)

    # Get spanning tree by computing BFS, starting at the current root.
    # NOTE(lkhamsurenl): Assume root is at (1, 1).
    spanning_tree = bfs(c_st.get_vertex((1, 1)))

    # Dual spanning tree. Note that we remove all edges in spanning tree and 2g auxiliary edges (which in our case:
    # (0, n-1) -> (0, 0) and (m-1, 0) -> (0, 0)).
    c_g = copy.deepcopy(graph)
    for v_name in spanning_tree:
        u_name = spanning_tree[v_name]
        if u_name != None:
            remove_edge(c_g.get_vertex(u_name), c_g.get_vertex(v_name))
    remove_edge(c_g.get_vertex((0, n - 1)), c_g.get_vertex((0, 0)))
    remove_edge(c_g.get_vertex((m - 1, 0)), c_g.get_vertex((0, 0)))

    # Compute dual spanning tree by computing BFS rooted at (0, 0) face.
    # NOTE(lkhamsurenl): Assume root is at face (0, 0).
    dual_spanning_tree = bfs(c_g.get_face((0, 0)))

    leafmost = compute_leafmost(dual_spanning_tree)
    for (u_name, v_name) in leafmost:
        if u_name != None:
            u = graph.get_face(u_name)
            v = graph.get_face(v_name)

            dart = u.neighbors[v]
            dart.weight = Weight(dart.weight.length, dart.weight.homology, leafmost[(u_name, v_name)])
            # Create reverse, dual, dual reverse respectively with corresponding leafmost terms.
            Edge(dart.tail, dart.head, dart.weight, dart.dual.tail, dart.dual.head)

    return graph


def g1():
    """
    Manually create 3 by 3 grid graph with genus 1.
    :return: Graph.
    """
    # Build vertices and faces.
    vertices = [[Vertex((i, j)) for j in range(3)] for i in range(3)]
    faces = [[Vertex((i, j)) for j in range(3)] for i in range(3)]

    # Build darts, its reverse, dual and dual reverse respectively.
    Edge(vertices[0][0], vertices[0][2], Weight(1, [-1, 0], 0), faces[0][2], faces[2][2])
    Edge(vertices[1][0], vertices[1][2], Weight(1, [-1, 0], 6), faces[1][2], faces[0][2])
    Edge(vertices[2][0], vertices[2][2], Weight(1, [-1, 0], 4), faces[2][2], faces[1][2])

    Edge(vertices[2][0], vertices[0][0], Weight(1, [0, -1], 0), faces[2][0], faces[2][2])
    Edge(vertices[2][2], vertices[0][2], Weight(1, [0, -1], -3), faces[2][2], faces[2][1])
    Edge(vertices[2][1], vertices[0][1], Weight(1, [0, -1], -1), faces[2][1], faces[2][0])

    Edge(vertices[0][0], vertices[1][0], Weight(1, [0, 0], -8), faces[0][0], faces[0][2])
    Edge(vertices[1][0], vertices[2][0], Weight(1, [0, 0], 1), faces[1][0], faces[1][2])
    Edge(vertices[0][2], vertices[1][2], Weight(1, [0, 0], -1), faces[0][2], faces[0][1])

    Edge(vertices[1][2], vertices[2][2], Weight(1, [0, 0], 0), faces[1][2], faces[1][1])
    Edge(vertices[0][1], vertices[1][1], Weight(1, [0, 0], 0), faces[0][1], faces[0][0])
    Edge(vertices[1][1], vertices[2][1], Weight(1, [0, 0], 0), faces[1][1], faces[1][0])

    Edge(vertices[0][2], vertices[0][1], Weight(1, [0, 0], 0), faces[0][1], faces[2][1])
    Edge(vertices[1][2], vertices[1][1], Weight(1, [0, 0], 0), faces[1][1], faces[0][1])
    Edge(vertices[2][2], vertices[2][1], Weight(1, [0, 0], -1), faces[2][1], faces[1][1])

    Edge(vertices[0][1], vertices[0][0], Weight(1, [0, 0], 0), faces[0][0], faces[2][0])
    Edge(vertices[1][1], vertices[1][0], Weight(1, [0, 0], 0), faces[1][0], faces[0][0])
    Edge(vertices[2][1], vertices[2][0], Weight(1, [0, 0], 0), faces[2][0], faces[1][0])

    return Graph(vertices=sum(vertices, []), faces=sum(faces, []))

def g2():
    """
    Manually create 6 by 6 grid graph with genus 2.
    :return: Graph.
    """
    # Build vertices and faces.
    vertices = [[Vertex((i, j)) for j in range(6)] for i in range(6)]
    faces = [[Vertex((i, j)) for j in range(6)] for i in range(6)]

    # Build darts, its reverse, dual and dual reverse respectively.
    Edge(vertices[0][0], vertices[0][1], Weight(1, [0, 0, 0, 0], 0), faces[5][0], faces[0][0])
    Edge(vertices[0][0], vertices[1][0], Weight(1, [0, 0, 0, 0], 0), faces[0][0], faces[0][5])
    Edge(vertices[1][0], vertices[1][1], Weight(1, [0, 0, 0, 0], 0), faces[0][0], faces[1][0])
    Edge(vertices[1][0], vertices[2][0], Weight(1, [0, 0, 0, 0], 0), faces[1][0], faces[1][5])
    Edge(vertices[2][0], vertices[2][1], Weight(1, [0, 0, 0, 0], 0), faces[1][0], faces[2][0])
    Edge(vertices[2][0], vertices[0][0], Weight(1, [0, -1, 0, 0], 0), faces[2][0], faces[2][5])
    Edge(vertices[0][0], vertices[3][1], Weight(1, [0, 1, 0, 0], 0), faces[2][0], faces[3][0])
    Edge(vertices[0][0], vertices[4][0], Weight(1, [0, 0, 0, 0], 0), faces[3][0], faces[3][5])
    Edge(vertices[4][0], vertices[4][1], Weight(1, [0, 1, 0, 0], 0), faces[3][0], faces[4][0])
    Edge(vertices[4][0], vertices[5][0], Weight(1, [0, 0, 0, 0], 0), faces[4][0], faces[4][5])
    Edge(vertices[5][0], vertices[5][1], Weight(1, [0, 1, 0, 0], 0), faces[4][0], faces[5][0])
    Edge(vertices[5][0], vertices[0][0], Weight(1, [0, 0, -1, 0], 0), faces[5][0], faces[5][5])


    Edge(vertices[0][1], vertices[0][2], Weight(1, [0, 0, 0, 0], 0), faces[5][1], faces[0][1])
    Edge(vertices[0][1], vertices[1][1], Weight(1, [0, 0, 0, 0], 0), faces[0][1], faces[0][0])
    Edge(vertices[1][1], vertices[1][2], Weight(1, [0, 0, 0, 0], 0), faces[0][1], faces[1][1])
    Edge(vertices[1][1], vertices[2][1], Weight(1, [0, 0, 0, 0], 0), faces[1][1], faces[1][0])
    Edge(vertices[2][1], vertices[2][2], Weight(1, [0, 0, 0, 0], 0), faces[1][1], faces[2][1])
    Edge(vertices[2][1], vertices[3][1], Weight(1, [0, 0, 0, 0], 0), faces[2][1], faces[2][0])
    Edge(vertices[3][1], vertices[3][2], Weight(1, [0, 0, 0, 0], 0), faces[2][1], faces[3][1])
    Edge(vertices[3][1], vertices[4][1], Weight(1, [0, 0, 0, 0], 0), faces[3][1], faces[3][0])
    Edge(vertices[4][1], vertices[4][2], Weight(1, [0, 0, 0, 0], 0), faces[3][1], faces[4][1])
    Edge(vertices[4][1], vertices[5][1], Weight(1, [0, 0, 0, 0], 0), faces[4][1], faces[4][0])
    Edge(vertices[5][1], vertices[5][2], Weight(1, [0, 0, 0, 0], 0), faces[4][1], faces[5][1])
    Edge(vertices[5][1], vertices[0][4], Weight(1, [0, -1, -1, 0], 0), faces[5][1], faces[5][0])


    Edge(vertices[0][2], vertices[0][0], Weight(1, [1, 0, 0, 0], 0), faces[5][2], faces[0][2])
    Edge(vertices[0][2], vertices[1][2], Weight(1, [0, 0, 0, 0], 0), faces[0][2], faces[0][1])
    Edge(vertices[1][2], vertices[1][3], Weight(1, [0, 0, 0, 0], 0), faces[0][2], faces[1][2])
    Edge(vertices[1][2], vertices[2][2], Weight(1, [0, 0, 0, 0], 0), faces[1][2], faces[1][1])
    Edge(vertices[2][2], vertices[2][3], Weight(1, [0, 0, 0, 0], 0), faces[1][2], faces[2][2])
    Edge(vertices[2][2], vertices[3][2], Weight(1, [0, 0, 0, 0], 0), faces[2][2], faces[2][1])
    Edge(vertices[3][2], vertices[3][3], Weight(1, [0, 0, 0, 0], 0), faces[2][2], faces[3][2])
    Edge(vertices[3][2], vertices[4][2], Weight(1, [0, 0, 0, 0], 0), faces[3][2], faces[3][1])
    Edge(vertices[4][2], vertices[4][3], Weight(1, [0, 0, 0, 0], 0), faces[3][2], faces[4][2])
    Edge(vertices[4][2], vertices[5][2], Weight(1, [0, 0, 0, 0], 0), faces[4][2], faces[4][1])
    Edge(vertices[5][2], vertices[5][3], Weight(1, [0, 0, 0, 0], 0), faces[4][2], faces[5][2])
    Edge(vertices[5][2], vertices[0][5], Weight(1, [0, -1, -1, 0], 0), faces[5][2], faces[5][1])

    Edge(vertices[0][0], vertices[0][4], Weight(1, [0, 0, 0, 0], 0), faces[5][3], faces[0][3])
    Edge(vertices[0][0], vertices[1][3], Weight(1, [-1, 0, 0, 0], 0), faces[0][3], faces[0][2])
    Edge(vertices[1][3], vertices[1][4], Weight(1, [0, 0, 0, 0], 0), faces[0][3], faces[1][3])
    Edge(vertices[1][3], vertices[2][3], Weight(1, [0, 0, 0, 0], 0), faces[1][3], faces[1][2])
    Edge(vertices[2][3], vertices[2][4], Weight(1, [0, 0, 0, 0], 0), faces[1][3], faces[2][3])
    Edge(vertices[2][3], vertices[3][3], Weight(1, [0, 0, 0, 0], 0), faces[2][3], faces[2][2])
    Edge(vertices[3][3], vertices[3][4], Weight(1, [0, 0, 0, 0], 0), faces[2][3], faces[3][3])
    Edge(vertices[3][3], vertices[4][3], Weight(1, [0, 0, 0, 0], 0), faces[3][3], faces[3][2])
    Edge(vertices[4][3], vertices[4][4], Weight(1, [0, 0, 0, 0], 0), faces[3][3], faces[4][3])
    Edge(vertices[4][3], vertices[5][3], Weight(1, [0, 0, 0, 0], 0), faces[4][3], faces[4][2])
    Edge(vertices[5][3], vertices[5][4], Weight(1, [0, 0, 0, 0], 0), faces[4][3], faces[5][3])
    Edge(vertices[5][3], vertices[0][0], Weight(1, [0, -1, -1, 1], 0), faces[5][3], faces[5][2])

    Edge(vertices[0][4], vertices[0][5], Weight(1, [0, 0, 0, 0], 0), faces[5][4], faces[0][4])
    Edge(vertices[0][4], vertices[1][4], Weight(1, [-1, 0, 0, 0], 0), faces[0][4], faces[0][3])
    Edge(vertices[1][4], vertices[1][5], Weight(1, [0, 0, 0, 0], 0), faces[0][4], faces[1][4])
    Edge(vertices[1][4], vertices[2][4], Weight(1, [0, 0, 0, 0], 0), faces[1][4], faces[1][3])
    Edge(vertices[2][4], vertices[2][5], Weight(1, [0, 0, 0, 0], 0), faces[1][4], faces[2][4])
    Edge(vertices[2][4], vertices[3][4], Weight(1, [0, 0, 0, 0], 0), faces[2][4], faces[2][3])
    Edge(vertices[3][4], vertices[3][5], Weight(1, [0, 0, 0, 0], 0), faces[2][4], faces[3][4])
    Edge(vertices[3][4], vertices[4][4], Weight(1, [0, 0, 0, 0], 0), faces[3][4], faces[3][3])
    Edge(vertices[4][4], vertices[4][5], Weight(1, [0, 0, 0, 0], 0), faces[3][4], faces[4][4])
    Edge(vertices[4][4], vertices[5][4], Weight(1, [0, 0, 0, 0], 0), faces[4][4], faces[4][3])
    Edge(vertices[5][4], vertices[5][5], Weight(1, [0, 0, 0, 0], 0), faces[4][4], faces[5][4])
    Edge(vertices[5][4], vertices[0][1], Weight(1, [0, -1, -1, 1], 0), faces[5][4], faces[5][3])

    Edge(vertices[0][5], vertices[0][0], Weight(1, [0, 0, 0, 1], 0), faces[5][5], faces[0][5])
    Edge(vertices[0][5], vertices[1][5], Weight(1, [-1, 0, 0, 0], 0), faces[0][5], faces[0][4])
    Edge(vertices[1][5], vertices[4][0], Weight(1, [1, 0, 0, 1], 0), faces[0][5], faces[1][5])
    Edge(vertices[1][5], vertices[2][5], Weight(1, [0, 0, 0, 0], 0), faces[1][5], faces[1][4])
    Edge(vertices[2][5], vertices[5][0], Weight(1, [1, 0, 0, 1], 0), faces[1][5], faces[2][5])
    Edge(vertices[2][5], vertices[3][5], Weight(1, [0, 0, 0, 0], 0), faces[2][5], faces[2][4])
    Edge(vertices[3][5], vertices[0][0], Weight(1, [1, 0, -1, 1], 0), faces[2][5], faces[3][5])
    Edge(vertices[3][5], vertices[4][5], Weight(1, [0, 0, 0, 0], 0), faces[3][5], faces[3][4])
    Edge(vertices[4][5], vertices[1][0], Weight(1, [1, 0, -1, 1], 0), faces[3][5], faces[4][5])
    Edge(vertices[4][5], vertices[5][5], Weight(1, [0, 0, 0, 0], 0), faces[4][5], faces[4][4])
    Edge(vertices[5][5], vertices[2][0], Weight(1, [1, 0, -1, 1], 0), faces[4][5], faces[5][5])
    Edge(vertices[5][5], vertices[0][2], Weight(1, [0, -1, -1, 1], 0), faces[5][5], faces[5][4])

    graph = Graph(vertices=sum(vertices, []), faces=sum(faces, []))

    # Num Edge(spanning tree) + Num edges(dual spanning tree) + 2 * g
    # Spanning tree in original graph. Note that we first remove non-trivial homology edges from graph prior to
    # computing spanning tree.
    # TODO(lkhamsurenl): Figure out a way to find Spanning tree without explicit copy of the entire graph.
    c_st = copy.deepcopy(graph)
    remove_edge(c_st.get_vertex((0, 2)), c_st.get_vertex((0, 0)))
    remove_edge(c_st.get_vertex((0, 0)), c_st.get_vertex((2, 0)))
    remove_edge(c_st.get_vertex((0, 0)), c_st.get_vertex((5, 0)))
    remove_edge(c_st.get_vertex((0, 5)), c_st.get_vertex((0, 0)))

    # Get spanning tree by computing BFS, starting at the current root.
    # NOTE(lkhamsurenl): Assume root is at (1, 1).
    spanning_tree = bfs(c_st.get_vertex((1, 1)))

    # Dual spanning tree. Note that we remove all edges in spanning tree and 2g auxiliary edges (which in our case:
    # (0, n-1) -> (0, 0) and (m-1, 0) -> (0, 0)).
    c_g = copy.deepcopy(graph)
    for v_name in spanning_tree:
        u_name = spanning_tree[v_name]
        if u_name != None:
            remove_edge(c_g.get_vertex(u_name), c_g.get_vertex(v_name))
    remove_edge(c_g.get_vertex((0, 2)), c_g.get_vertex((0, 0)))
    remove_edge(c_g.get_vertex((0, 0)), c_g.get_vertex((2, 0)))
    remove_edge(c_g.get_vertex((0, 0)), c_g.get_vertex((5, 0)))
    remove_edge(c_g.get_vertex((0, 5)), c_g.get_vertex((0, 0)))

    # Compute dual spanning tree by computing BFS rooted at (0, 0) face.
    # NOTE(lkhamsurenl): Assume root is at face (0, 0).
    dual_spanning_tree = bfs(c_g.get_face((0, 0)))

    leafmost = compute_leafmost(dual_spanning_tree)
    for (u_name, v_name) in leafmost:
        if u_name != None:
            u = graph.get_face(u_name)
            v = graph.get_face(v_name)

            dart = u.neighbors[v]
            dart.weight = Weight(dart.weight.length, dart.weight.homology, leafmost[(u_name, v_name)])
            # Create reverse, dual, dual reverse respectively with corresponding leafmost terms.
            Edge(dart.tail, dart.head, dart.weight, dart.dual.tail, dart.dual.head)

    return graph
