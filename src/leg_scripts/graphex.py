import networkx as nx

G = nx.Graph()

G.add_edge(1,2)
G.add_edge(1,2)

print len(G.edges())
