import matplotlib.pyplot as plt
import networkx as nx

L=4

G = nx.grid_2d_graph(L -1 ,L - 1)
#nx.draw(G,node_size=200)


G2 = nx.DiGraph(G)


for n,nbrsdict in G2.adjacency_iter():
    for nbr,eattr in nbrsdict.items():
        (x1, y1) = n
        (x2, y2) = nbr
        print "({}, {}) -> ({}, {})".format(x1 % L, y1 % L,  x2 % L, y2 % L)

nx.draw_spectral(G2,node_size=600,node_color='w', with_labels=True)
plt.show()