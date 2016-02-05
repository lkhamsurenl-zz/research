from src.model.graph import Graph

g = Graph()
a = g.addVertex("a")
b = g.addVertex("b")

a.addEdge(b, 1)

print(a.neighbors[b])
print(b.neighbors)