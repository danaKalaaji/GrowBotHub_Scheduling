import sys
import edges
import optimization as opti
import plants_array as plants
import graph_construction_and_draw as gc

###  OUTPUTS  ###

# Writes the outputs in two different files :
# output.txt which contains all the instructions that the robotic arm will have to perform
# output2.txt which contains the states of all the growth modules for each day
def write_outputs():
	total_plants = 0
	for e in gc.g.edges:
		if e[0].type == 'source' and e[1].type == 'module':
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0:
					total_plants += opti.flow_vars[e[0], e[1], p].varValue
	return total_plants
