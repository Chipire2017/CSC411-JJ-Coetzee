import matplotlib.pyplot as plt
import networkx as nx
import sympy as sy
from sympy.parsing.sympy_parser import parse_expr

#-------------------------------------------------------------------------
# Extraction of Equations and Graph Creation
eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open('eqns.txt')]
unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]

G = nx.MultiDiGraph()

for unkn in unkns:
    for curr_node in range(0,len(eqns)):
        if unkn in eqns[curr_node]:
            for next_node in range(curr_node,len(eqns)):
                if unkn in eqns[next_node]:
                    if G.has_edge(curr_node,next_node):
                        G.add_edge(next_node,curr_node,weight=1,label=str(unkn))
                    else:
                        weight = 0.5
                    G.add_edge(next_node, curr_node, weight=weight, label=str(unknown))

#-------------------------------------------------------------------
# Tarjan Algorithm and Symbolic Solving of Equations

Tarjan = nx.strongly_connected_components(G)
simu = []

Tarjan.reverse()

for curr in Tarjan:
    for now in curr:
        simu.append(eqns[now])
    soln = sy.solve(simu,unkns)
    print soln

print Tarjan


#--------------------------------------------------------------------
# Drawing of Graph

pos = nx.spring_layout(G)
sypy = sy.sympify(eqns)
sol = sy.solve(sypy, unkns)

print sol

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos)

plt.axis('off')
plt.show()
