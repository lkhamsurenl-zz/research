import matplotlib.pyplot as plt
import networkx as nx
L=4

G = nx.grid_2d_graph(L,L)
#nx.draw(G,node_size=200)


G2 = nx.DiGraph(G)
# for edge in G2.edges():
#     if edge != tuple(sorted(edge)):
#         G2.remove_edge(*edge)



for n,nbrsdict in G2.adjacency_iter():
    for nbr,eattr in nbrsdict.items():
        print "({},{})".format(n % (L -1), nbr % (L - 1), 1)

nx.draw_spectral(G2,node_size=600,node_color='w', with_labels=True)
plt.show()