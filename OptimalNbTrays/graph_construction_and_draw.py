from matplotlib.pyplot import savefig
import networkx as nx
import edges

###  GRAPH CONSTRUCTION AND DRAW  ###

# The graph
g = None
# The positions of all the nodes in the graph g
pos = None

## CONSTRUCTION ##

# This function adds all the edges created before to the graph g
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


# Sub-function which creates the dictionnary that contains all the node positions to draw the graph g
def get_node_pos(g):
    pos = dict()
    for node in g.nodes:
        pos[node] = (node.when, node.where)
    return pos

# Sub-function which adds an edge to the graph g
def add_edge_to_graph(e):
    edge = (e.node_from, e.node_to)
    g.add_edge(*edge, bounds=e.bounds, size=e.size)