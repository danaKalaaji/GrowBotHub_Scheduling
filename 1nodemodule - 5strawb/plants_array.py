import inputs

###  PLANTS ARRAY  ###

# Array of tuple (plant data, first day)
plants = None

'''
Creates the array that holds ll the comodities: a tuple (plant data, first day) for each
type of plants and for each possible day
'''
def all_plants():
	global plants
	plants = []

	for plant in inputs.plant_data:
		# Cannot seed a plant if it has not the time to grow
		for day in range(inputs.HORIZON + 1 - plant.total_days):
			plants.append((plant, day))

'''
#force a strawberry every 5 days
def all_plants():
	global plants
	plants = []

	for plant in inputs.plant_data:
		# Cannot seed a plant if it has not the time to grow
		for day in range(inputs.HORIZON + 1 - plant.total_days):
			if (plant.name == "Strawberry" and day % 5 == 0) or plant.name != "Strawberry":
			plants.append((plant, day))
'''