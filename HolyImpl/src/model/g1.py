from src.model.dart import Dart
from src.model.edge import Edge
from src.model.vertex import Vertex
from src.model.weight import Weight
from src.model.graph import Graph

from collections import deque
__author__ = 'Luvsandondov Lkhamsuren'

class G1:
    # genus 1 grid of 3 x 3
    def __init__(self):
        a = Vertex("a")
        b = Vertex("b")
        c = Vertex("c")
        d = Vertex("d")
        e = Vertex("e")
        f = Vertex("f")
        g = Vertex("g")
        h = Vertex("h")
        k = Vertex("k")
        vertices = [a, b, c, d, e, f, g, h, k]

        # Build the dual graph.
        m = Vertex("M")
        n = Vertex("N")
        l = Vertex("L")
        t = Vertex("T")
        u = Vertex("U")
        w = Vertex("W")
        x = Vertex("X")
        y = Vertex("Y")
        z = Vertex("Z")
        faces = [m, n, l, t, u, w, x, y, z]

        # Build darts and duals
        ae = Dart(a, e, Weight(1, [-1,0], 0))
        bf = Dart(b, f, Weight(1, [-1,0], 6))
        cg = Dart(c, g, Weight(1, [-1,0], 4))
        ea = ae.create_reverse_dart()
        fb = bf.create_reverse_dart()
        gc = cg.create_reverse_dart()

        ca = Dart(c, a, Weight(1, [0,-1], 0))
        ge = Dart(g, e, Weight(1, [0,-1], -3))
        kd = Dart(k, d, Weight(1, [0,-1], -1))
        ac = ca.create_reverse_dart()
        eg = ge.create_reverse_dart()
        dk = kd.create_reverse_dart()

        ab = Dart(a, b, Weight(1, [0,0], -8))
        bc = Dart(b, c, Weight(1, [0,0], 1))
        ef = Dart(e, f, Weight(1, [0,0], -1))
        ba = ab.create_reverse_dart()
        cb = bc.create_reverse_dart()
        fe = ef.create_reverse_dart()

        fg = Dart(f, g, Weight(1, [0,0], 0))
        dh = Dart(d, h, Weight(1, [0,0], 0))
        hk = Dart(h, k, Weight(1, [0,0], 0))
        gf = fg.create_reverse_dart()
        hd = dh.create_reverse_dart()
        kh = hk.create_reverse_dart()

        ed = Dart(e, d, Weight(1, [0,0], 0))
        fh = Dart(f, h, Weight(1, [0,0], 0))
        gk = Dart(g, k, Weight(1, [0,0], -1))
        de = ed.create_reverse_dart()
        hf = fh.create_reverse_dart()
        kg = gk.create_reverse_dart()

        da = Dart(d, a, Weight(1, [0,0], 0))
        hb = Dart(h, b, Weight(1, [0,0], 0))
        kc = Dart(k, c, Weight(1, [0,0], 0))
        ad = da.create_reverse_dart()
        bh = hb.create_reverse_dart()
        ck = kc.create_reverse_dart()

        # Generate face edges
        lm = Dart(l, m, Weight(1, [1, 0], 0))
        mn = Dart(m, n, Weight(1, [1, 0], -6))
        nl = Dart(n, l, Weight(1, [1, 0], -4))
        ml = lm.create_reverse_dart()
        mn = mn.create_reverse_dart()
        nl = nl.create_reverse_dart()

        tu = Dart(t, u, Weight(1, [0, 0], 0))
        uw = Dart(u, w, Weight(1, [0, 0], 1))
        wt = Dart(w, t, Weight(1, [0, 0], 0))
        ut = tu.create_reverse_dart()
        wu = uw.create_reverse_dart()
        tw = wt.create_reverse_dart()

        xy = Dart(x, y, Weight(1, [0, 0], 0))
        yz = Dart(y, z, Weight(1, [0, 0], 0))
        zx = Dart(z, x, Weight(1, [0, 0], 0))
        yx = xy.create_reverse_dart()
        zy = yz.create_reverse_dart()
        xz = zx.create_reverse_dart()

        mt = Dart(m, t, Weight(1, [0, 0], -1))
        tx = Dart(t, x, Weight(1, [0, 0], 0))
        xm = Dart(x, m, Weight(1, [0, 0], -8))
        tm = mt.create_reverse_dart()
        xt = tx.create_reverse_dart()
        mx = xm.create_reverse_dart()

        nu = Dart(n, u, Weight(1, [0, 0], 0))
        uy = Dart(u, y, Weight(1, [0, 0], 0))
        yn = Dart(y, n, Weight(1, [0, 0], 1))
        un = nu.create_reverse_dart()
        yu = uy.create_reverse_dart()
        lm = ml.create_reverse_dart()

        lw = Dart(l, w, Weight(1, [0, -1], -3))
        wz = Dart(w, z, Weight(1, [0, -1], -1))
        zl = Dart(z, l, Weight(1, [0, -1], 0))
        wl = lw.create_reverse_dart()
        zw = wz.create_reverse_dart()
        lz = zl.create_reverse_dart()

        self.graph = Graph(vertices=vertices, faces=faces)

    def initial_tree(self, source):
        """
        :return: Predecessor pointer for initial holy tree.
        """
        pred = {source: None}
        dist = {} # distance for each Vertex
        visited = {} # keep track of which vertices we visited.
        # Initialize the distance values.
        dist[source] = Weight(homology=[0,0])
        for v in self.graph.vertices:
            if v != source:
                dist[v] = Weight(length=float('inf'))

        queue = deque()
        queue.appendleft(source)
        while len(queue) != 0:
            u = queue.pop()
            visited[u] = 1
            for v in u.neighbors.keys():
                if v not in visited:
                    queue.appendleft(v)
                if dist[u] + u.neighbors[v].weight < dist[v]:
                    #du = dist[u]
                    #dv = dist[v]
                    #dist[v] = Weight(du.length + dv.length, [i + j for (i, j) in zip(du.homology, dv.homology)], \
                    #                 du.leafmost + dv.leafmost)
                    print("dist[{0}] = {1}; weight = {2}; dist[{3}] = {4}".format(u, dist[u], u.neighbors[v].weight, v, dist[v]))
                    dist[v] = dist[u] + u.neighbors[v].weight

                    pred[v] = u

        return (pred, dist)

g1 = G1()
s = g1.graph.get_vertex("h")
(pred, dist) = g1.initial_tree(s)
for u in pred.keys():
    pu = pred[u] if pred[u] != None else "None"
    dpu = dist[pred[u]] if pred[u] != None and dist[pred[u]] != None else "None"
    du = dist[u] if dist[u] != None else "None"
    print("{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}".format(pu, u, dpu, du))
