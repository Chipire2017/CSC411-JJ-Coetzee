#2013-02-11
#2013-02-16

import matplotlib.pyplot as plt
import networkx as nx
import sympy as sy
from sympy.parsing.sympy_parser import parse_expr

#-------------------------------------------------------------------------
# Extraction of Equations and Graph Creation
eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open('eqns.txt')]
unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
edge_data = []
unknown = ''

listunkn = {}
#print unkn
#print eqns

G = nx.MultiDiGraph()

for unknown in unkns:
    for curr_node, eqn in enumerate(eqns):
        if unknown in eqn:
            for next_node in range(curr_node, len(eqns)):
                eqn2 = eqns[next_node]
                if unknown in eqn2:
                    if G.has_edge(curr_node, next_node):
                        weight = 1
                    else:
                        weight = 0.5
                    G.add_edge(next_node, curr_node, weight=weight, label=str(unknown))


#-------------------------------------------------------------------
# Tarjan Algorithm and Symbolic Solving of Equations

Tarjan = nx.strongly_connected_components(G)
soln = 0
simu = []
teller = 0
Tarjan.reverse()
eqan = []

for curr in Tarjan:
    for now in curr:
        simu.append(eqns[now])
    eqan = sy.sympify(simu)
    soln = sy.solve(eqan, unkns)
    print soln

print Tarjan
#print listunkn

#--------------------------------------------------------------------
# Drawing of Graph

pos = nx.spring_layout(G)
sypy = sy.sympify(eqns)
sol = sy.solve(sypy, unkns)

print sol

nx.draw_networkx(G, pos)
nx.draw_networkx_edge_labels(G, pos)
#nx.draw_spring(G)

plt.axis('off')
#plt.savefig('Structure DiGraph')
plt.show()
