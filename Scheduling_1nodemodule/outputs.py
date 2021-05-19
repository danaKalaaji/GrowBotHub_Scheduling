import sys

import inputs
import edges
import optimization as opti
import plants_array as plants
import graph_construction_and_draw as gc
import pandas as pd
from classes import Instruction

###  OUTPUTS  ###

# Writes the outputs in two different files :
# output.txt which contains all the instructions that the robotic arm will have to perform
# output2.txt which contains the states of all the growth modules for each day
def write_outputs():
	total_plants = 0
	original_stdout = sys.stdout
	
	# Writing the instructions output
	f = open("output.txt", "w")
	sys.stdout = f

	instructions = [[] for i in range(inputs.HORIZON + 2)]

	# Three types of instructions (See the Instruction() class in the classes.py file)
	for e in gc.g.edges:
		if e[0].type == 'hole' and e[1].type == 'hole' and e[0].where != e[1].where:
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0:

					instructions[e[1].when].append(Instruction(p[0].name, opti.flow_vars[e[0], e[1], p].varValue,'hole_transfer', e[0].hole,
															   e[0].tray, e[1].hole, e[1].tray))
		if e[0].type == 'source' and e[1].type == 'hole':
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0:
					instructions[e[1].when].append(Instruction(
						p[0].name, opti.flow_vars[e[0], e[1], p].varValue, 'source_transfer', e[1].hole, e[1].tray))
					total_plants += opti.flow_vars[e[0], e[1], p].varValue

		if e[0].type == 'hole' and e[1].type == 'sink':
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0:
					instructions[e[0].when + 1].append(Instruction(
						p[0].name, opti.flow_vars[e[0], e[1], p].varValue, 'sink_transfer', e[0].hole, e[0].tray))


	for i in range(len(instructions)):
		print("DAY " + str(i))
		for s in instructions[i]:
			print(s.toString())	

	sys.stdout = original_stdout
	f.close()


		# Writing the growth modules states output
	f = open("output2.txt", "w")

	states = [[[] for i in range(inputs.HORIZON + 1)] for k in range(len(inputs.TRAYS))]

	for e in gc.g.edges:
		if e[1].type == 'hole':
			for p in plants.plants:
				if (e[0].type != 'source' or e[1].when == 0) and (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0:
					states[e[1].tray][e[1].when].append(
						"Hole : " + str(e[1].hole) + " | Plant : " + p[0].name)

	sys.stdout = f
	for i in range(len(states)):
		print("GROWTH MODULE " + str(i))
		for j in range(len(states[i])):
			if(len(states[i][j]) != 0):
				print("DAY " + str(j))
				for k in range(len(states[i][j])):
					print(states[i][j][k])

	sys.stdout = original_stdout
	f.close()
	print("total number of plants is:", total_plants)





	f = open("output_compare.txt", "w")
	sys.stdout = f
	for i in range(len(instructions)):
		print("DAY " + str(i))
		for s in instructions[i]:
			for i in range(int(s.number)):
				print(s.toString_compare())	

	sys.stdout = original_stdout
	f.close() 


	#	Day by day what plants we are harvesting + For each type of plants the day it is being harvested
	f = open("output_harvested.txt", "w")
	sys.stdout = f
	harvested = [[] for p in range(edges.n_plants)]
	frame_plant =[[0]*len(instructions) for p in range(edges.n_plants)]

	for i in range(len(instructions)):
		print("DAY " + str(i))
		for s in instructions[i]:
			if s.type == 'sink':
				print("Day " + str(i) + ": " +s.toString())
				for j in range(edges.n_plants):
					if s.name == inputs.plant_data[j].name:
						harvested[j].append((s, i))
						frame_plant[j][i] = int(s.number)
	print("_____________________________________________________________________________________")

	for i in range(len(harvested)):
		if harvested[i]:
			print(harvested[i][0][0].name + ":")
			for j in range(len(harvested[i])):
				s, day = harvested[i][j]
				print("Day " + str(day) + ": " + s.toString())
			print("\n")

	print("_____________________________________________________________________________________")
	df = pd.DataFrame(frame_plant, index = [p.name for p in inputs.plant_data])
	pd.set_option('display.max_rows', None)
	pd.set_option('display.max_columns', None)
	print(df.transpose())



	sys.stdout = original_stdout
	f.close()
	

