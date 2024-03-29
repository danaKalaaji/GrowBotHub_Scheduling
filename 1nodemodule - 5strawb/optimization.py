import pulp as plp
from pulp.constants import LpMaximize

import graph_construction_and_draw as gc
import inputs
import plants_array as plants
import edges

###  OPTIMIZATION  ###

# Creates the Pulp model and ask to maximize it
model = plp.LpProblem(name="Scheduling", sense=plp.LpMaximize)
# The flow variables of the model
flow_vars = None

## FLOW VARIABLES ##

'''
Creates the flow variables using the graph edges computed before.
Each edge connecting a node of type A has a
    -total capacity = number of holes per growth modules
    -capacity per commodity of 2
'''
def make_flow_vars():
    # Set those two variables as global
    global flow_vars
    global model

    flow_vars = dict()
    for u, v, d in gc.g.edges(data=True):
        for key, val in d['bounds'].items():
            if(val > 0):
                flow_vars[u, v, key] = plp.LpVariable(name='{}_{}_{}'.format(
                    *(u, v, key)), lowBound=0, upBound=inputs.HOLES, cat='Integer')
                # Per-commodity capacity constraints
                model += flow_vars[u, v, key] <= 2

        # Bundle constraints: total capacity
        bundle = []
        bundle += [flow_vars[u, v, key]
                   for key in d['bounds'].keys() if (u, v, key) in flow_vars]
        model += plp.lpSum(bundle) <= inputs.HOLES

## SIZE CONSTRAINT ##

'''
##OLD CONSTRAINT
# Adds the size constraint to the model :
# The sum of the sizes of two neighbor plants should not exceed MAX_SIZE (defined in inputs.py)
def size_constraint():
    global model
    for max_size in inputs.MAX_SIZE.keys():
        for pair in (pair for pair in pair_of_neighbors(gc.g) if (pair[0].module_number, pair[1].module_number) in inputs.MAX_SIZE[max_size]):
            bundle = []
            for e in (e for e in gc.g.in_edges(pair[0], data=True) if e[0].type == 'module'):
                for c in e[2]['size'].keys():
                    if (e[0], pair[0], c) in flow_vars:
                        bundle += [flow_vars[e[0], pair[0], c]
                                   * e[2]['size'].get(c)]
            for e in (e for e in gc.g.in_edges(pair[1], data=True) if e[0].type == 'module'):
                for c in e[2]['size'].keys():
                    if (e[0], pair[1], c) in flow_vars:
                        bundle += [flow_vars[e[0], pair[1], c]
                                   * e[2]['size'].get(c)]
            model += plp.lpSum(bundle) <= max_size
'''

## NEW CONSTRAINT
'''
Adds the size constraint to the model.
There cannot be more than 2 big plants (Lettuce, Cabbage, Fennel) in each module of type 2.
'''
def size_constraint():
    global model
    lettuce_fennel_module = []
    lettuce_cabbage_module = []
    fennel_cabbage_module = []

    for n in (n for n in gc.g.nodes if n.type == 'module'):
        if n.module_type == 2:
            for e in (e for e in gc.g.in_edges(n)): #if e[0].type == 'module'):
                for c in plants.plants:
                    if (e[0], e[1], c) in flow_vars:
                        if c[0].name == "Lettuce":
                            lettuce_fennel_module += [flow_vars[e[0], e[1], c]]
                            lettuce_cabbage_module += [flow_vars[e[0], e[1], c]]
                        elif c[0].name == "Cabbage":
                            lettuce_cabbage_module += [flow_vars[e[0], e[1], c]]
                            fennel_cabbage_module += [flow_vars[e[0], e[1], c]]
                        elif c[0].name == "Fennel":
                            lettuce_cabbage_module += [flow_vars[e[0], e[1], c]]
                            fennel_cabbage_module += [flow_vars[e[0], e[1], c]]
        model += plp.lpSum(lettuce_fennel_module) <= 2
        model += plp.lpSum(lettuce_cabbage_module) <= 2
        model += plp.lpSum(fennel_cabbage_module) <= 2
        lettuce_fennel_module = []
        lettuce_cabbage_module = []
        fennel_cabbage_module = []


## MAXIMUM INFLOW CONSTRAINT ##

'''
Adds the maximum inflow constraint to the model :
The inflow for all nodes in the graph (except sources ans sinks) should not exceed the number of holes per growth modules
(Maximum one plant per hole)
For each node, for each one of its incoming edge and for each (plant, day); if (plant, day) goes through the edge, adds its flow to the array.
'''
def max_inflow_constraint():
    global model
    inflow_from_holes = [[] for _ in range(len(gc.g.nodes))]
    for n in (n for n in gc.g.nodes if n.type == 'module'):
        for e in (e for e in gc.g.in_edges(n)): #if e[0].type == 'module'):
            for c in plants.plants:
                if (e[0], e[1], c) in flow_vars:
                    inflow_from_holes[list(gc.g.nodes).index(n)] += [flow_vars[e[0], e[1], c]]
                    #print(e[0].module_type, e[0].module_number, e[0].when , "||",e[1].module_type, e[1].module_number, e[1].when, "||",flow_vars[e[0], e[1], c].varValue)

        model += plp.lpSum(inflow_from_holes[list(gc.g.nodes).index(n)]) <= inputs.HOLES



## FLOW CONSERVATION CONSTRAINT ##

'''
Adds the flow conservation constraint to the model :
Inflow and outflow of a node (except sources and sinks) should be equal
'''
def flow_conservation_constraint():
    global model
    for n in (n for n in gc.g.nodes if n.type == 'module'):
        for c in plants.plants:
            inflow, outflow = get_inflow_outflow(gc.g, flow_vars, n, c)
            model += inflow - outflow == 0



## BALANCE CONSTRAINT ##

'''
Adds the balance constraint to the model :
The number of plants of a certain type produced should be larger or equal to the limit minus a loose up constraint alpha
  -limit : The number of plant produced divided by the number of types of plant
  -alpha : Set to 4 manually here (but can be changed). This constant allows the constraint to be less strict
'''
def balance_constraint():
    global model
    alpha = 4
    sink_inflow = get_sink_inflow_balance_constraint()
    limit = (plp.lpSum(sink_inflow) / edges.n_plants) - alpha
    for n in [n for n in gc.g.nodes if n.sink]:
        sink = []
        for e in gc.g.in_edges(n):
            for c in plants.plants:
                if (e[0], e[1], c) in flow_vars:
                    if c[0].name == "Strawberry":
                        sink += 5*[flow_vars[e[0], e[1], c]]
                    else:
                        sink += [flow_vars[e[0], e[1], c]]
        model += plp.lpSum(sink) >= limit


## OPTIMIZE ##

'''
Asks the solver to maximize the number of plant produced in this model
Can choose to authorize or not to put a timeout to the optimization
'''
def optimize():
    global model
    w = 7
    model += plp.lpSum(get_sink_inflow()) - w* plp.lpSum(z()) #- v * plp.lpSum(y())

    # Solves without timeout
    #model.solve()

    # Solves With a cut of of fracGap
    model.solve(plp.PULP_CBC_CMD(fracGap = 0.05))

    # Solves With a timeout of MAX_TIME minutes
    #model.solve(plp.PULP_CBC_CMD(maxSeconds=inputs.MAX_TIME * 60))


## SUB-FUNCTIONS ##

'''
# Sub-function that creates all the pairs of neighbor nodes in the graph
def pair_of_neighbors(g):
    pairs = set()
    for n1 in (n1 for n1 in gc.g.nodes if n1.type == 'module' and n1.where % 2 == 0):
        for n2 in (n2 for n2 in gc.g.nodes if n1.neighbors(n2)):
            pairs.add((n1, n2))
    return pairs
'''


'''
Calculates the inflow and outflow for each node in the graph (except sources and sinks)
'''
def get_inflow_outflow(g, flow_v, n, c):
    inflow = 0
    outflow = 0
    for e in g.in_edges(n):
        if (e[0], e[1], c) in flow_vars:
            inflow += plp.lpSum([flow_v[e[0], e[1], c]])
    for e in g.out_edges(n):
        if (e[0], e[1], c) in flow_vars:
            outflow += plp.lpSum([flow_v[e[0], e[1], c]])
    return inflow, outflow



'''
Calculates the inflow of all sinks in the graph with a strawberry constraint.
Each time we have one strawberry, it considers that we have 5 strawberries
'''
def get_sink_inflow_balance_constraint():
    sink_inflow_balance_constraint = []
    for n in [n for n in gc.g.nodes if n.sink]:

        for e in gc.g.in_edges(n):
            for c in plants.plants:
                if (e[0], e[1], c) in flow_vars:
                    if c[0].name == "Strawberry":
                        sink_inflow_balance_constraint += 5*[flow_vars[e[0], e[1], c]]
                    else:
                        sink_inflow_balance_constraint += [flow_vars[e[0], e[1], c]]
    return sink_inflow_balance_constraint


'''
Calculates the inflow of all sinks in the graph without the strawberry constraint
'''
def get_sink_inflow():
    sink_inflow = []
    for n in [n for n in gc.g.nodes if n.sink]:

        for e in gc.g.in_edges(n):
            for c in plants.plants:
                if (e[0], e[1], c) in flow_vars:
                    sink_inflow += [flow_vars[e[0], e[1], c]]
    return sink_inflow
    
'''
Diversity constraint: one plant per day.
For each day d, z[d] is
    - 0 if we harvest a plant on day d
    - 1 otherwise
Puts a weight on day d if no plants were harvested that day
'''
def z():
    global model
    z = [plp.LpVariable(name='{}'.format(d), lowBound=0, upBound=1, cat='Integer') for d in range(inputs.HORIZON+1)]
    flow_per_day = [[] for _ in range(inputs.HORIZON+1)]

    # Sum flows for each day
    for n in [n for n in gc.g.nodes if n.sink]:
        for e in gc.g.in_edges(n):
            for c in plants.plants:
                if (e[0], e[1], c) in flow_vars:
                    d = e[0].when
                    flow_per_day[d] += [flow_vars[e[0], e[1], c]]

    # Add constraint for each day
    for d in range(60, inputs.HORIZON):
        model += z[d] >= 1 - plp.lpSum(flow_per_day[d])

    return z


#constraint: at most x plants of type p every 3 days --> weight if we harvest plants of type p more than once every 3 days
"""
def y():
    global model
    y = dict()
    for e in gc.g.edges:
        y[e[0],e[1]] = plp.LpVariable(name='{}_{}'.format(*(e[0],e[1])), lowBound=0, upBound=1, cat='Integer')

    for c in plants.plants:
        # Condition 1
        for e in gc.g.edges:
            if (e[0], e[1], c) in flow_vars:
                model += flow_vars[e[0], e[1], c] <= 5*y[e[0],e[1]]

        #Condition 2
    sum_ys = dict()
    for d in range(60, inputs.HORIZON+1):
        for c in plants.plants:
            sum_ys[c,d] = []

    for n in [n for n in gc.g.nodes if n.sink]:
        for e in gc.g.in_edges(n):
            for c in plants.plants:
                d = e[0].when
                if d > 62:
                    sum_ys[c,d] += [y[e]]
                    if d-1 >= 0:
                        sum_ys[c,d-1] += [y[e]]
                    if d-2 >= 0:
                        sum_ys[c,d-2] += [y[e]]

    for sum_y in list(sum_ys.values()):
        model += plp.lpSum(sum_y) <= 1

    return list(y.values()) """