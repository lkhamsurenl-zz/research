from src.model.dart import Dart
from src.model.edge import Edge
from src.model.vertex import Vertex
from src.model.weight import Weight
from src.model.graph import Graph

__author__ = 'Luvsandondov Lkhamsuren'

class G1(Graph):
    # genus 1 grid of 3 x 3
    def __init__(self):
        a = Vertex((0,0))
        b = Vertex((1,0))
        c = Vertex((2,0))
        d = Vertex((0,1))
        e = Vertex((0,2))
        f = Vertex((1,2))
        g = Vertex((2,2))
        h = Vertex((1,1))
        k = Vertex((2,1))
        vertices = [a, b, c, d, e, f, g, h, k]

        # Build the dual graph.
        m = Vertex((0,2))
        n = Vertex((1,2))
        l = Vertex((2,2))
        t = Vertex((0,1))
        u = Vertex((1,1))
        w = Vertex((2,1))
        x = Vertex((0,0))
        y = Vertex((1,0))
        z = Vertex((2,0))
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

        self.vertices = vertices
        self.faces = faces