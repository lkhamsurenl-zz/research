from collections import deque

def bfs(source):
    """
    Return pred dictionary with vertices name map.
    :param source:
    :return: pred{source name -> dest name}
    """
    pred = {source.name: None}
    visited = {} # Keeps track of which vertices are visited.
    queue = deque()
    queue.appendleft(source)
    while len(queue) != 0:
        u = queue.pop()
        for v in u.neighbors.keys():
            if v not in visited:
                pred[v.name] = u.name
                queue.appendleft(v)
        visited[u] = 1 # mark as visited.
    return pred

def dfs(source):
    pred = {source: None}
    visited = {}
    s = [] # stack used for recursion
    s.append(source)
    while len(s) != 0:
        u = s[-1]
        visited[u] = 1 # mark as visited
        for v in u.neighbors.keys():
            if v not in visited:
                pred[v] = u
                s.append(v)
                break
        if u == s[-1]:
            # If u is still on top of stack, all neighbors of u were visited. So simply remove u from s.
            s.pop()
    return pred