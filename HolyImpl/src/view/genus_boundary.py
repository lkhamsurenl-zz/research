# genus_boundary includes functions handle duplication of edges in visualization.

def get_vertex_mapping(g, m, n):
    """
    Compute the vertex mapping (resolve duplication of boundary for visualization).
    :param g: Genus of graph embedding surface.
    :param m: Width of the grid.
    :param n: Height of the grid.
    :return:
    """
    assert g < 3, "For now, genus can be at most 2."
    vertex_mapping = {}
    # Each vertex mapping includes map to itself.
    for i in range(m):
        for j in range(n):
            vertex_mapping[(i, j)] = [(i, j)]
    if g == 1:
        for i in range(m + 1):
            vertex_mapping[(i % m, 0)].append((i, n))
        for j in range(n + 1):
            vertex_mapping[(0, j % n)].append((m, j))
    else:
        vertex_mapping[(0,0)] += [(3,0), (6,0), (0,3), (6,3), (0,6), (3,6), (6,6)]

        vertex_mapping[(1,0)].append((4,6))
        vertex_mapping[(2,0)].append((5,6))
        vertex_mapping[(4,0)].append((1,6))
        vertex_mapping[(5,0)].append((2,6))

        vertex_mapping[(0,1)].append((6,4))
        vertex_mapping[(0,2)].append((6,5))
        vertex_mapping[(0,4)].append((6,1))
        vertex_mapping[(0,5)].append((6,2))

    return vertex_mapping

def get_face_mapping(g, m, n):
    """
    Compute the face mapping (resolve duplication of boundary for visualization).
    :param g: Genus of graph embedding surface.
    :param m: Width of the grid.
    :param n: Height of the grid.
    :return:
    """
    face_mapping = {}
    # Non-boundary face mapping
    for i in range(m):
        for j in range(n):
            face_mapping[(i, j)] = [(i + 1, j + 1)]
    if g == 1:
        for i in range(m):
            face_mapping[(i, 0)].append((i + 1, n + 1))
            face_mapping[(i, n - 1)].append((i + 1, 0))
        for j in range(n):
            face_mapping[(0, j)].append((m + 1, j + 1))
            face_mapping[(m - 1, j)].append((0, j + 1))
    elif g == 2:
        face_mapping[(0,0)] = [(1,1), (4,7), (7, 4)]
        face_mapping[(3,5)].append((1,0))
        face_mapping[(4,5)].append((2,0))
        face_mapping[(0,5)] += [(4,0), (7, 3)]
        face_mapping[(1,5)].append((5,0))
        face_mapping[(2,5)].append((6,0))

        face_mapping[(5,3)].append((0,1))
        face_mapping[(5,4)].append((0,2))
        face_mapping[(5,5)] += [(0,3), (3,0)]
        face_mapping[(5,0)] += [(0,4), (3, 7)]
        face_mapping[(5,1)].append((0,5))
        face_mapping[(5,2)].append((0,6))

        face_mapping[(0, 3)].append((7, 1))
        face_mapping[(0, 4)].append((7, 2))
        face_mapping[(0, 1)].append((7, 5))
        face_mapping[(0, 2)].append((7, 6))

        face_mapping[(3, 0)].append((1, 7))
        face_mapping[(4, 0)].append((2, 7))
        face_mapping[(1, 0)].append((5, 7))
        face_mapping[(2, 0)].append((6, 7))

    return face_mapping

def resolve_boundary_darts(us, vs):
    """
    Boundary darts must be duplicated and resolved. For instance, (0, 0) -> (2, 0) must be resolved to
    { (3, 0) -> (2, 0), (2, 3) -> (3, 3) } when m = 3, n = 3
    :param us: Tail vertex name (its boundary duplicates).
    :param vs: Head vertex name (its boundary duplicates).
    :return: All possible duplicates of (u_name -> v_name).
    """
    duplicates = []
    for tail in us:
        for heaad in vs:
            # Return only valid darts (vertex that are connected.)
            if abs(tail[0] - heaad[0]) + abs(tail[1] - heaad[1]) == 1:
                duplicates.append((tail, heaad))
    return duplicates

def expand_vertices_list(ls, mapping):
    """
    :param ls: List to expand.
    :param mapping: {(i, j) -> [(i, j), (x, y), (a, b), etc]}
    :return:
    """
    # Expanded list.
    expanded_list = []
    for vertex in ls:
        if vertex in mapping:
            expanded_list += mapping[vertex]

    return expanded_list
