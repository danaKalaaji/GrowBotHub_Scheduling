from inputs import read_inputs
from plants_array import all_plants
from edges import *
from graph_construction_and_draw import *
from optimization import *
from outputs import write_outputs

import time

start_time = time.time()


def total_plants_given_trays(TRAYS_PER_TYPE, HOLES, model):
	###  GRAPH CONSTRUCTION  ###

	# Creates the array of tuple (plant data, first day) which contains all possible plants (commodities)
	all_plants()

	# Creates the source and sink of the graph for each type of plant
	make_meta_nodes()

	# Creates the edges that stay in the same growth module
	make_tray_edges()

	# Creates the edges that change of growth modulemodel.solve(plp.PULP_CBC_CMD(maxSeconds=inputs.MAX_TIME * 60))
	make_transfer_edges()

	# Creates the edges that connect the sources with the growth modules
	make_source_edges()

	# Creates the edges that connect the growth modules to the sinks
	make_sink_edges()

	# Constructs the graph with all the edges we created
	construction()

	###  OPTIMIZATION  ###

	# Creates the flow variables and set the per-commodity capacity constraint and the bundle constraint
	make_flow_vars(TRAYS_PER_TYPE, HOLES, model)

	# Set the sizes constraint
	#size_constraint()

	# Set the maximum inflow to a hole to HOLES
	max_inflow_constraint(HOLES, model)

	# Set the flow conservation constraint
	flow_conservation_constraint(model)

	# Set the balance constraint
	balance_constraint(model)

	# Start to optimize to find an optimal solution with Pulp
	optimize(model)

	###  COMPUTE OUTPUT  ###

	# Write the outputs in two different files
	result = int(write_outputs())

	print(TRAYS_PER_TYPE, result)
	return result

