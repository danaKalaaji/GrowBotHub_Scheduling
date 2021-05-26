import inputs
import total_plants_given_trays
import edges
import pulp as plp

import itertools

global HOLES
global TRAYS_PER_TYPE

# Read the inputs from a file and set all the parameters
inputs.read_inputs()
models = [plp.LpProblem(name="Scheduling", sense=plp.LpMaximize) for _ in range((inputs.MAX_TRAYS+1) ** inputs.TRAYS)]
index = 0

max_total_plants, best_trays_per_type = 0, []

for TRAYS_PER_TYPE in itertools.product(range(inputs.MAX_TRAYS+1),repeat=inputs.TRAYS):
	if sum(TRAYS_PER_TYPE) <= inputs.MAX_TRAYS:
		HOLES = [nb_trays * 5 for nb_trays in TRAYS_PER_TYPE]
		current_total_plant = total_plants_given_trays.total_plants_given_trays(TRAYS_PER_TYPE, HOLES, models[index])
		index += 1
		if current_total_plant == max_total_plants:
			best_trays_per_type.append(TRAYS_PER_TYPE)
		elif current_total_plant > max_total_plants:
			max_total_plants = current_total_plant
			best_trays_per_type = [TRAYS_PER_TYPE]



print("=======================================")
print("Max plants:", max_total_plants)
print("With TRAYS_PER_TYPE:", best_trays_per_type)