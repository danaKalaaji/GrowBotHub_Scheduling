from matplotlib.pyplot import savefig
import networkx as nx
import matplotlib.pyplot as plt

import edges
import plants_array as plants
import optimization as opti

##  GRAPH CONSTRUCTION AND DRAW  ##

# The graph
g = None
# The positions of all the nodes in the graph g
pos = None


'''
Construction of the graph.
Adds all the edges created before to the graph g
'''
def construction():
	
	global pos
	global g
	g = nx.DiGraph()

	for edge in edges.tray_edges:
		add_edge_to_graph(edge)
	for edge in edges.transfer_edges:
		add_edge_to_graph(edge)
	for edge in edges.source_edges:
		add_edge_to_graph(edge)
	for edge in edges.sink_edges:
		add_edge_to_graph(edge)
		pos = get_node_pos(g)


'''
Draws the graph before the optimization and put it in the graph.png file
'''
def draw_non_opti():
	fig = plt.figure(figsize=(15, 8))
	nx.draw(g, pos=pos, node_size=60, node_color='red', edgecolors='w', width=.3, linewidths=2, edge_color='grey')
	savefig("graph.png")
	print("Done with graph")



'''
Draws the graph after optimization and shows the paths of all the plants (see optimized.png)
'''
def draw_opti():
	fig = plt.figure(figsize=(20, 12))
	limits = plt.axis("off")  # turn off axis

	nx.draw_networkx_nodes(g, pos, node_size=60,
						   node_color='red', edgecolors='w', linewidths=2)

	for e in g.edges:
		# a list of plants that have flow on the edge
		plant_through = []
		for p in plants.plants:
			if((e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0):
				plant_through += [p]
		if len(plant_through):
			plant_type = plant_through[0][0]
			g.edges[e[0], e[1]]['color'] = 'c'
		else:
			g.edges[e[0], e[1]]['color'] = 'grey'


	edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'grey']
	nx.draw_networkx_edges(g, pos, edgelist, edge_color='grey', width=.3)

	edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] != 'grey']
	edgelabels = {edge: int(sum([opti.flow_vars[edge[0], edge[1], p].varValue if (edge[0], edge[1], p) in opti.flow_vars 
		else 0 for p in plants.plants])) for edge in edgelist}
	nx.draw_networkx_edges(g, pos, edgelist, edge_color='c', width=.3)	
	nx.draw_networkx_edge_labels(g, pos, edgelabels, font_size=5)

	savefig("optimized.png")
	print("Done with optimized graph")



## SUB-FUNCTIONS ##

'''
Creates the dictionnary that contains all the node positions to draw the graph g
'''
def get_node_pos(g):
    pos = dict()
    for node in g.nodes:
        pos[node] = (node.when, node.where)
    return pos

'''
Adds an edge to the graph g
'''
def add_edge_to_graph(e):
    edge = (e.node_from, e.node_to)
    g.add_edge(*edge, bounds=e.bounds, size=e.size)