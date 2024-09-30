
import matplotlib.pyplot as plt
import networkx as nx

# Create the graph
G = nx.DiGraph()

# Add nodes with the node attribute "bipartite"
G.add_node('Symptoms', bipartite=0, color='blue')
G.add_node('Diagnostic Tests', bipartite=1, color='yellow')
G.add_node('Positive Result/Prescriptions', bipartite=1, color='green')

# Add edges
G.add_edges_from([('Symptoms', 'Diagnostic Tests'), ('Diagnostic Tests', 'Positive Result/Prescriptions')])

# Separate by group: symptoms, diagnostic tests, prescriptions
l, r = nx.bipartite.sets(G)
pos = {}

# Update position for node from each group
pos.update((node, (1, index)) for index, node in enumerate(l))
pos.update((node, (2, index)) for index, node in enumerate(r))

# draw the nodes: blue for symptoms, yellow for diagnostic tests, green for prescriptions
nx.draw(G, pos, with_labels=True, node_color=[G.nodes[node]['color'] for node in G.nodes()])

# display
plt.show()
