import inputs

###  ALL THE CLASSES  ###


'''
NODE CLASS : This class defines a node of the graph

Parameters of a node :
    where (int): gives the position on the graph to be able to draw it
    when (int): gives the time that this node represent (if it is a 'modules')
    sink (boolean): true only if the node is a sink
    type (string): the type of the node (modules, source, sink)
If the node is of type 'modules' :
    modules_type (int): gives the type of the modules represented by the node (from 0 to NB_TYPE_MODULE)
'''
class Node(object):
    def __init__(self, *args):

        #('modules', modules_type, when)
        if args[0] == 'modules':
            self.where = args[1]*2
            self.when = args[2]
            self.sink = False
            self.type = 'modules'
            self.modules_type = args[1]

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

'''
        # True if the two holes are neighbors
    def neighbors(self, other):
        return self.type == 'modules' and other.type == 'modules' and self.when == other.when and abs(self.where - other.where) == 1
'''

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
        return Node('sink', inputs.NB_TYPE_MODULE * 2 + 1, size)




'''
INSTRUCTION CLASS : This class defines an instruction that the robotic arm will have to perform

Parameters of an instruction :
    name (string): the name of the plant
    number (int): number of plants to be transfered (flow per commodity)
    type (string): the type of the transfer (module, source, sink)
For a module transfer :
    type_from (int): the growth module type from which the plant comes
    type_to (int): the growth module type in which the plant goes
For a source transfer :
    type_to (int): the growth module type in which the plant goes
For a sink transfer :
    type_from (int): the growth module type in which the plant goes
'''

class Instruction():
    def __init__(self, name, number, *args):
        self.name = name
        self.number = number
        if args[0] == 'module_transfer':
            self.tray_from = args[1]
            self.tray_to = args[2]
            self.type = 'modules'

        elif args[0] == 'source_transfer':
            self.tray_to = args[1]
            self.type = 'source'

        elif args[0] == 'sink_transfer':
            self.tray_from = args[1]
            self.type = 'sink'

        # Return the instruction as a string that will be put in the output.txt file for the robotic arm
    def toString(self):
        if(self.type == 'modules'):
            return "Move " + str(int(self.number))  + " " +self.name + " from tray " + str(self.tray_from) + " to tray " + str(self.tray_to)
        elif(self.type == 'source'):
            return "Plant " + str(int(self.number)) + " seed of " + self.name + " in tray " + str(self.tray_to)
        else:
            return "Harvest " + str(int(self.number)) + " plant " + self.name + " from tray " + str(self.tray_from)

    def toString_compare(self):
        if(self.type == 'modules'):
            return "Move "  + " " +self.name + " from tray " + str(self.tray_from) + " to tray " + str(self.tray_to)
        elif(self.type == 'source'):
            return "Plant "  + " seed of " + self.name + " in tray " + str(self.tray_to)
        else:
            return "Harvest " + " plant " + self.name + " from tray " + str(self.tray_from)

