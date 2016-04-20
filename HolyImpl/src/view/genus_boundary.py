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
    face_mapping = get_vertex_mapping(g, m, n)
    # Mapping of face is slightly different when g = 2.
    if g == 2:
        face_mapping[(0,0)] = [(0, 0), (3,6), (6, 3)]
        face_mapping[(0,3)] = [(0, 3), (6,0)]
        face_mapping[(3,0)] = [(3, 0), (0,6)]

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
    for i in us:
        for j in vs:
            # Return only valid darts (vertex that are connected.)
            if abs(i[0] - j[0]) + abs(i[1] - j[1]) == 1:
                duplicates.append((i, j))
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
