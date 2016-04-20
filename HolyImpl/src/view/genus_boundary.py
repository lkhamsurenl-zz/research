def get_vertex_mapping(g, m, n):
    """
    Compute the vertex mapping (resolve duplication of boundary for visualization).
    :param g:
    :param m:
    :param n:
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

def resolve_boundary_darts(us, vs):
    """
    Boundary darts must be duplicated and resolved. For instance, (0, 0) -> (2, 0) must be resolved to
    { (3, 0) -> (2, 0), (2, 3) -> (3, 3) } when m = 3, n = 3
    :param us: Tail vertex name (its boundary duplicates).
    :param vs: Head vertex name (its boundary duplicates).
    :param m: Width of the grid graph.
    :param n: Height of the grid graph.
    :return: All possible duplicates of (u_name -> v_name).
    """
    duplicates = []
    for i in us:
        for j in vs:
            if abs(i[0] - j[0]) + abs(i[1] - j[1]) == 1:
                duplicates.append((i, j))
    return duplicates