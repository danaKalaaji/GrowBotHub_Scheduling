import inputs
import numpy as np

###  ALL THE CLASSES  ###


'''
NODE CLASS : This class defines a node of the graph

Parameters of a node :
    where (int): gives the position on the graph to be able to draw it
    when (int): gives the time that this node represent (if it is a 'module')
    sink (boolean): true only if the node is a sink
    type (string): the type of the node (module, source, sink)
If the node is of type 'module' :
    module_type (int): gives the type of the module (from 0 to NB_TYPE_MODULE)
    module_number (int): gives the number of the module (from 0 to MODULES[type of module])
'''


class Node(object):
    def __init__(self, *args):

        #('module', module_type, module_number, when)
        if args[0] == 'module':
            self.where = args[1] * (np.amax(inputs.MODULES)+2) + args[2]
            self.when = args[3]
            self.sink = False
            self.type = 'module'
            self.module_type = args[1]
            self.module_number = args[2]

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

        # True if the two module are neighbors
    def neighbors(self, other):
        return self.type == 'module' and other.type == 'module' and self.when == other.when and abs(self.where - other.where) == 1

    def __eq__(self, other):
        return self.where == other.where and self.when == other.when and self.type == other.type

    def __hash__(self):
        return hash((self.where, self.when, self.type))




'''
PLANT CLASS : This class defines a plant in our system

Parameters of a plant:
    name (string): the name of the plant
    total_days (int): the total number of days, from the seeding to the harvesting
    size(list): array storing for each day the size of the plant
    transfers(list): list of the growth module in which the plant has to pass (in the list order)
    transfer_days(list): array that gives the number of days the plant has to stay in each growth module
'''

class Plant():
    def __init__(self, name, total_days, size, transfers, transfer_days):
        self.name = name
        self.total_days = total_days
        self.size = size
        self.transfers = transfers
        self.transfer_days = transfer_days

        # Source of the plant
    def source(self, size):
        return Node('source', -3, size)

        # Sink of the plant
    def sink(self, size):
        return Node('sink', inputs.NB_TYPE_MODULE * (np.amax(inputs.MODULES) + 2) + 1, size)





'''
INSTRUCTION CLASS : This class defines an instruction that the robotic arm will have to perform

Parameters of an instruction :
    name (string): the name of the plant
    number (int): number of plants 
    type (string): the type of the transfer (module, source, sink)
For a module transfer :
    type_from (int): the growth module type from which the plant comes
    module_from (int): the module from which the plant comes
    type_to (int): the growth module type in which the plant goes
    module_to (int): the module in which the plant goes
For a source transfer :
    type_to (int): the growth module type in which the plant goes
    module_to (int): the module in which the plant goes
For a sink transfer :
    type_from (int): the growth module type in which the plant goes
    module_from (int): the module in which the plant goes
'''

class Instruction():
    def __init__(self, name, number,*args):
        self.name = name
        self.number = number
        if args[0] == 'module_transfer':
            self.module_from = args[1]
            self.module_type_from = args[2]
            self.module_to = args[3]
            self.module_type_to = args[4]
            self.type = 'module'

        elif args[0] == 'source_transfer':
            self.hole_to = args[1]
            self.module_type_to = args[2]
            self.type = 'source'

        elif args[0] == 'sink_transfer':
            self.module_from = args[1]
            self.module_type_from = args[2]
            self.type = 'sink'


        # Return the instruction as a string that will be put in the output.txt file for the robotic arm
    def toString(self):
        if(self.type == 'module'):
            return "Move " + str(int(self.number))  + " "  + self.name + " from module_type " + str(self.module_type_from) + " to module_type " + str(self.module_type_to)
        elif(self.type == 'source'):
            return "Plant " + str(int(self.number)) + " seed of "  + self.name + " in module_type " + str(self.module_type_to)
        else:
            return "Harvest " + str(int(self.number)) + " plant " + self.name + " from module_type " + str(self.module_type_from)


'''
    def toString_compare(self):
        if(self.type == 'module'):
            return "Move " + self.name + " from module_type " + str(self.module_type_from) + " to module_type " + str(self.module_type_to)
        elif(self.type == 'source'):
            return "Plant seed of " + self.name + " in module_type " + str(self.module_type_to)
        else:
            return "Harvest plant " + self.name + " from module_type " + str(self.module_type_from)
'''