import classes
from collections import defaultdict


###  INPUTS ###

'''
All the inputs (given by data.txt) are global variables
Reads the data.txt file and sets all the plant data (using the Plant class in classes.py)
and the global variables described above
'''
def read_inputs():

    # All types of plants
    global plant_data
    # Array with the number of modules for each type of growth module
    global MODULES
    # Total number of types of modules
    global NB_TYPE_MODULE
    # Number of holes for each growth module
    global HOLES
    # Number of days we have to produce a maximum of plants
    global HORIZON
    
    # The sum of the sizes of two neighbor plants should not exceed MAX_SIZE
    #global MAX_SIZE
    # Optimization timeout is set at MAX_TIME minutes
    #global MAX_TIME

    f = open("data.txt", "r")

    plant_data = []
    #MAX_SIZE = defaultdict(list)

    for x in f:
        data = x.replace(" ", "")
        data = data.split("|")

        if data[0] == "MODULES":
            MODULES = list(map(int, data[1].split(";")))
            NB_TYPE_MODULE = len(MODULES)
            HOLES = 5

        elif data[0] == "HORIZON":
            HORIZON = int(data[1])

        elif data[0] == "PLANT":
            name = data[1]
            total_days = int(data[2])
            #sizes = list(map(int, data[4].split(",")))
            first_day = 0
            pairs = data[3].split(";")

            sizes = []
            for p in pairs:
                size, last_day = (int(val) for val in p.split(","))
                for d in range (first_day, last_day):
                    sizes.append(size)
                first_day = last_day

            transfers = list(map(int, data[4].split(",")))
            transfer_days = []
            days = data[5].split(";")
            for d in days:
                transfer_days.append(list(map(int, d.split(","))))

            plant_data.append(
                classes.Plant(name, total_days, sizes, transfers, transfer_days))

  
    '''   
        elif data[0] == "MAX_TIME":
            MAX_TIME = int(data[1])

        elif data[0] == "MAX_SIZE":
            constraints = data[1].split(";")

            for c in constraints:
                info_data = c.split(":")
                sizes = info_data[1].split("-")

                for s in sizes:
                    bounds = s.split(",")
                    MAX_SIZE[int(info_data[0])].append(
                        (int(bounds[0]), int(bounds[1])))
                    MAX_SIZE[int(info_data[0])].append(
                        (int(bounds[1]), int(bounds[0])))
    '''
    f.close()
