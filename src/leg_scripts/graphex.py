import networkx as nx

G = nx.Graph()

G.add_edge(1,2, {'weight':1})

print len(G.edges())
print G[1][2]
print G.has_edge(1,3)
print G[1][2]['weight']
G[1]['hello'] = False
print G[1]['hello']
