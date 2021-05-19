import inputs

###  ALL THE CLASSES  ###

## NODE CLASS ##

# This class defines a node of the graph

# Arguments of a module :
# - where : gives the position on the graph to be able to draw it
# - when : gives the time that this node represent (if it is a 'module')
# - sink : true only if the node is a sink
# - type : the type of the node (module, source, sink)
# If the node is of type 'module' :
# - tray : gives the tray 


class Node(object):
    def __init__(self, *args):

        #('module', tray, when)
        if args[0] == 'module':
            self.where = args[1]*2
            self.when = args[2]
            self.sink = False
            self.type = 'module'
            self.tray = args[1]

        #('source', where, when)
        elif args[0] == 'source':
            self.where = args[1]
            self.when = args[2]
            self.sink = False
            self.type = 'source'

        #('sink', where, when)
        elif args[0] == 'sink':
            self.where = args[1]
            self.when = args[2]
            self.sink = True
            self.type = 'sink'

        # True if the two holes are neighbors
    def neighbors(self, other):
        return self.type == 'module' and other.type == 'module' and self.when == other.when and abs(self.where - other.where) == 1

    def __eq__(self, other):
        return self.where == other.where and self.when == other.when and self.type == other.type

    def __hash__(self):
        return hash((self.where, self.when, self.type))

## PLANT CLASS ##

# This class defines a plant in our system

# Arguments of a plant :
# - name : the name of the plant
# - total_days : the total number of days, from the seeding to the harvesting
# - color : the color of the plant on the optimized graph
# - size : the different sizes in time of the plant
# - transfers : list of the growth module in which the plant has to pass (in the list order)
# - transfer_days : gives the number of days the plant has to stay in each growth module


class Plant():
    def __init__(self, name, total_days, color, size, transfers, transfer_days):
        self.name = name
        self.total_days = total_days
        self.color = color
        self.size = size
        self.transfers = transfers
        self.transfer_days = transfer_days

        # Source of the plant
    def source(self, size):
        return Node('source', -3, size)

        # Sink of the plant
    def sink(self, size):
        return Node('sink', inputs.TRAYS * 2 + 1, size)

## INSTRUCTION CLASS ##

# This class defines an instruction that the robotic arm will have to perform

# Arguments of an instruction :
# - name : the name of the plant
# - number : number of plants to be transfered (flow of a particular plant)
# - type : the type of the transfer (module, source, sink)
# For a module transfer :
# - tray_from : the growth module from which the plant comes
# - tray_to : the growth module in which the plant goes
# Arguments for the source and sink transfers mean the same as the arguments for module transfers


class Instruction():
    def __init__(self, name, number, *args):
        self.name = name
        self.number = number
        if args[0] == 'module_transfer':
            self.tray_from = args[1]
            self.tray_to = args[2]
            self.type = 'module'

        elif args[0] == 'source_transfer':
            self.tray_to = args[1]
            self.type = 'source'

        elif args[0] == 'sink_transfer':
            self.tray_from = args[1]
            self.type = 'sink'

        # Return the instruction as a string that will be put in the output.txt file for the robotic arm
    def toString(self):
        if(self.type == 'module'):
            return "Move " + str(int(self.number))  + " " +self.name + " from tray " + str(self.tray_from) + " to tray " + str(self.tray_to)
        elif(self.type == 'source'):
            return "Plant " + str(int(self.number)) + " seed of " + self.name + " in tray " + str(self.tray_to)
        else:
            return "Harvest " + str(int(self.number)) + " plant " + self.name + " from tray " + str(self.tray_from)

    def toString_compare(self):
        if(self.type == 'module'):
            return "Move "  + " " +self.name + " from tray " + str(self.tray_from) + " to tray " + str(self.tray_to)
        elif(self.type == 'source'):
            return "Plant "  + " seed of " + self.name + " in tray " + str(self.tray_to)
        else:
            return "Harvest " + " plant " + self.name + " from tray " + str(self.tray_from)

