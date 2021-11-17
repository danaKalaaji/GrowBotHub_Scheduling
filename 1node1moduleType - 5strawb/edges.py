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



'''
An edge is defined by:
	node_from and node_to (Node): the two nodes that this edge connects
	bounds (plants, value): with value = [0,1] (cf function "get_bounds_per_edge")
	size (int): size of the active plant 
'''
Edge = namedtuple('Edge', ['node_from', 'node_to', 'bounds', 'size'])



## GROWTH MODULE EDGES ##
'''
Creates all the edges that stay in the same growth module type from a day to another.
For each module and for each day, createss an edge that connects this module type to the 
same module type on the next day and store it in the array tray_edges
'''
def make_tray_edges():
	number_tray_edges = 0
	global tray_edges
	tray_edges = []
	for modules_type in range(inputs.NB_TYPE_MODULE):
		for t in range(inputs.HORIZON):
			node_from = classes.Node('modules', modules_type, t)
			node_to = classes.Node('modules', modules_type, t + 1)
			edge = Edge(node_from, node_to, get_bounds_per_edge(modules_type, t, plants_array.plants), get_sizes_per_edge(modules_type, t, plants_array.plants))
			tray_edges.append(edge)
			number_tray_edges += 1
	print("number_tray_edges:", number_tray_edges)
		


## TRANSFER EDGES ##  
'''
Creates all the transfer edges: for all possible plants (plant type, day it is seeded) and
for each one of its transfers from a module of type A to a module of type B, creates an
edge that connects all modules of type A to all modules of type B and stores it in the array 
transfer_edges
'''
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

			node_from = classes.Node('modules', from_, t)

			node_to = classes.Node('modules', to_, t+1)
			edge = Edge(node_from, node_to, get_bounds_per_edge(
				to_, t, plants_array.plants), get_sizes_per_edge(to_, t, plants_array.plants))
			transfer_edges.append(edge)
			number_transfer_edges += 1
	print("number_transfer_edges:", number_transfer_edges)



## SOURCE EDGES ##  
'''
Creates all the source edges : for each source it creates its node and then connect an creates all
the edges that comes from this source and stores it in the array source_edges.
'''
def make_source_edges():  
	number_source_edges  = 0
	global source_edges            
	source_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]
		modules_type = plant_type.transfers[0]
		bounds = {p: 1*(p == plant) for p in plants_array.plants}

		source = meta_nodes[get_plant_type(plant_type)][0]
		node_to = classes.Node('modules', modules_type, plant[1])
		edge = Edge(source, node_to, bounds, 0)
		source_edges.append(edge)
		number_source_edges +=1
	print("number_source_edges:", number_source_edges)	



## SINK EDGES ##  
'''
Creates all the sink edges : for each sink it creates its node and then connect an creates all
the edges that goes to this source and stores it in the array sink_edges.
'''
def make_sink_edges():
	number_sink_edges = 0    
	global sink_edges  
	sink_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]
		size_tray = len(plant_type.transfers)
		modules_type = plant_type.transfers[size_tray - 1]
		bounds = {p: 1*(p == plant) for p in plants_array.plants}

		sink = meta_nodes[get_plant_type(plant_type)][1]

		node_from = classes.Node('modules', modules_type,
						 plant[1] + plant_type.total_days)
		edge = Edge(node_from, sink, bounds, 0)
		sink_edges.append(edge)
		number_sink_edges += 1
	print("number_sink_edges:", number_sink_edges)	



## SUB-FUNCTIONS ##


'''
Returns True if the plant goes in a growth module of type module_type
during its life
Parameters:
	module_type (int): the type of module we are considering
	plant (Plant): the plant we are considering
'''
def isTrayInPlant(modules_type, plant):
	return modules_type in plant.transfers


'''
Gives the index of the growth module type for a certain plant
Parameters:
	module_type (int): the type of module of which we want the index
	plant (Plant): the plant we are considering
'''
def get_tray_index(modules_type, plant):
    return plant.transfers.index(modules_type)

'''
Computes all the bounds for each type of plant at a given time and in a
given growth module type. Bounds are 0 or 1:
	0 = This plant cannot be on this edge
	1 = This plant can be on this edge
For all possible plants (plant type, day it was seeded), if it goes to a module of type 
module_type on day t, then its bound value is 1 (else it is 0).
Parameters:
	module_type (int): the module type considered
	t (int): the day considered
	plants: array containing all the plants (plant type, day it was seeded)
'''
def get_bounds_per_edge(modules_type, t, plants):
    bounds_dict = dict()
    for plant in plants:
        day = plant[1]
        this_plant = plant[0]
        if isTrayInPlant(modules_type, this_plant):
            day_from = day + \
                this_plant.transfer_days[get_tray_index(modules_type, this_plant)][0]
            day_to = day + \
                this_plant.transfer_days[get_tray_index(
                    modules_type, this_plant)][1] - 1
            bounds_dict[plant] = (day_from <= t <= day_to)*1
        else:
            bounds_dict[plant] = 0
    return bounds_dict

'''
Returns an array containing all the sizes for each type of plant at a given time and in a 
given growth module type
Parameters:
	module_type (int): the module type considered
	t (int): the day considered
	plants: array containing all the plants (plant type, day it is seeded)
'''
def get_sizes_per_edge(modules_type, t, plants):
    sizes_dict = dict()
    for plant in plants:
        day = plant[1]
        plant_type = plant[0]

        sizes_dict[plant] = 0

        if isTrayInPlant(modules_type, plant_type):
            day_from = day + \
                plant_type.transfer_days[get_tray_index(modules_type, plant_type)][0]
            day_to = day + \
                plant_type.transfer_days[get_tray_index(
                    modules_type, plant_type)][1] - 1

            if day_from <= t <= day_to:
                sizes_dict[plant] = plant_type.size[t - day]

    return sizes_dict

'''
Returns the type of a given plant
Parameters:
	plant (Plant): plant considered
'''
def get_plant_type(plant):
	for i in range(n_plants):
		if(inputs.plant_data[i].name == plant.name):
			return i 
	return -1
 
'''
Creates the array that contains all the meta nodes (sources and 
sinks) for all types of plant
'''
def make_meta_nodes():
	global n_plants
	n_plants = len(inputs.plant_data)
	size = inputs.HORIZON / (n_plants-1)
	
	global meta_nodes
	meta_nodes = []
	for i in range(n_plants):
		meta_nodes.append((inputs.plant_data[i].source(size * i),
						   inputs.plant_data[i].sink(size * i)))



