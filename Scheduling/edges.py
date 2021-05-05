from collections import namedtuple
import inputs
import classes
import plants_array

###  EDGES  ###

# All the edges, the meta nodes (sources and sinks) and the number of plants are global variables
tray_edges = None
transfer_edges = None
source_edges = None
sink_edges = None
meta_nodes = None
n_plants = None



# An edge is defined by :
# - node_from and node_to : the  two nodes that this edge connects
# - bounds : (plants, value)  value = [0,1]
# - size : size of the active plant (int)
Edge = namedtuple('Edge', ['node_from', 'node_to', 'bounds', 'size'])



## GROWTH MODULE EDGES ##

# Creates all the edges that stay in the same growth module
# WARNING : We can add the diagonal edges (see comments in the code)
def make_tray_edges():
	number_tray_edges = 0
	global tray_edges
	tray_edges = []
	for tray in range(inputs.TRAYS):
		for hole in range(inputs.HOLES):
			for t in range(inputs.HORIZON):
			# WITHOUT DIAGONAL EDGES #
				node_from = classes.Node('hole', tray, hole, t)
				node_to = classes.Node('hole', tray, hole, t + 1)
				edge = Edge(node_from, node_to, get_bounds_per_edge(tray, t, plants_array.plants), get_sizes_per_edge(tray, t, plants_array.plants))
				tray_edges.append(edge)
				number_tray_edges += 1
	print("number_tray_edges:", number_tray_edges)
			# WITHOUT DIAGONAL EDGES #
			# WITH DIAGONAL EDGES #
				#node_from = classes.Node('hole', tray, hole, t)
				#for hole_to in range(inputs.HOLES):
					#node_to = classes.Node('hole',tray, hole_to, t + 1)
					#edge = Edge(node_from, node_to, get_bounds_per_edge(tray, t, plants_array.plants), get_sizes_per_edge(tray, t, plants_array.plants))
					#tray_edges.append(edge)
			# WITH DIAGONAL EDGES #
			
## TRANSFER EDGES ##  

# Creates all the edges that change of growth module
def make_transfer_edges(): 
	number_transfer_edges = 0   
	global transfer_edges     
	transfer_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]

		for i in range(len(plant_type.transfers) - 1):

			from_ = plant_type.transfers[i]
			to_ = plant_type.transfers[i + 1]

			t = plant_type.transfer_days[i][1] + plant[1]
			for hole in range(inputs.HOLES):
				node_from = classes.Node('hole', from_, hole, t)

				for hole_to in range(inputs.HOLES):
					node_to = classes.Node('hole', to_, hole_to, t+1)
					edge = Edge(node_from, node_to, get_bounds_per_edge(
						to_, t, plants_array.plants), get_sizes_per_edge(to_, t, plants_array.plants))
					transfer_edges.append(edge)
					number_transfer_edges += 1
	print("number_transfer_edges:", number_transfer_edges)


## SOURCE EDGES ##  

# Creates all the edges that come from the sources
def make_source_edges():  
	number_source_edges  = 0
	global source_edges            
	source_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]
		tray = plant_type.transfers[0]
		bounds = {p: 1*(p == plant) for p in plants_array.plants}

		source = meta_nodes[get_plant_type(plant_type)][0]

		for hole in range(inputs.HOLES):
			node_to = classes.Node('hole', tray, hole, plant[1])
			edge = Edge(source, node_to, bounds, 0)
			source_edges.append(edge)
			number_source_edges +=1
	print("number_source_edges:", number_source_edges)	

## SINK EDGES ##  

# Creates all the edges that got to the sinks
def make_sink_edges():
	number_sink_edges = 0    
	global sink_edges  
	sink_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]
		size_tray = len(plant_type.transfers)
		tray = plant_type.transfers[size_tray - 1]
		bounds = {p: 1*(p == plant) for p in plants_array.plants}

		sink = meta_nodes[get_plant_type(plant_type)][1]

		for hole in range(inputs.HOLES):
			node_from = classes.Node('hole', tray, hole,
							 plant[1] + plant_type.total_days)
			edge = Edge(node_from, sink, bounds, 0)
			sink_edges.append(edge)
			number_sink_edges += 1
	print("number_sink_edges:", number_sink_edges)	


# Sub-function : True if the plant goes in this growth module (tray) during her life
def isTrayInPlant(tray, plant):
    return tray in plant.transfers

# Sub-function : Gives the index of the growth module (tray) for a certain plant
def get_tray_index(tray, plant):
    return plant.transfers.index(tray)

# Sub-function : Computes all the bounds  for each type of plant at a given time and in a given growth module (bounds are 0 or 1)
# 0 = This plant cannot be on this edge
# 1 = This plant can be on this edge
def get_bounds_per_edge(tray, t, plants):
    bounds_dict = dict()
    for plant in plants:
        day = plant[1]
        this_plant = plant[0]
        if isTrayInPlant(tray, this_plant):
            day_from = day + \
                this_plant.transfer_days[get_tray_index(tray, this_plant)][0]
            day_to = day + \
                this_plant.transfer_days[get_tray_index(
                    tray, this_plant)][1] - 1
            bounds_dict[plant] = (day_from <= t <= day_to)*1
        else:
            bounds_dict[plant] = 0
    return bounds_dict

# Sub-function : Computes all the sizes for each type of plant at a given time and in a given growth module
def get_sizes_per_edge(tray, t, plants):
    sizes_dict = dict()
    for plant in plants:
        day = plant[1]
        plant_type = plant[0]

        sizes_dict[plant] = 0

        if isTrayInPlant(tray, plant_type):
            day_from = day + \
                plant_type.transfer_days[get_tray_index(tray, plant_type)][0]
            day_to = day + \
                plant_type.transfer_days[get_tray_index(
                    tray, plant_type)][1] - 1

            if day_from <= t <= day_to:
                sizes_dict[plant] = plant_type.size[t - day]

    return sizes_dict

# Sub-function : returns the type of a given plant
def get_plant_type(plant):
	for i in range(n_plants):
		if(inputs.plant_data[i].name == plant.name):
			return i 
	return -1
 
# Sub-function that creates the array that contains all the meta nodes (sources and sinks) for all types of plant
def make_meta_nodes():
	global n_plants
	n_plants = len(inputs.plant_data)
	size = inputs.HORIZON / (n_plants-1)
	
	global meta_nodes
	meta_nodes = []
	for i in range(n_plants):
		meta_nodes.append((inputs.plant_data[i].source(size * i),
						   inputs.plant_data[i].sink(size * i)))



