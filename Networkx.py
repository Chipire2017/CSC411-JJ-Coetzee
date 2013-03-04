<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
try:
    import matplotlib.pyplot as plt
except:
    raise

=======
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
#2013-02-11
#2013-02-16

import matplotlib.pyplot as plt
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
import networkx as nx
import sympy as sy
from sympy.parsing.sympy_parser import parse_expr

#-------------------------------------------------------------------------
# Extraction of Equations and Graph Creation
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
eqns = [line.strip() for line in open('eqns.txt')]
unkns = symbols([line.strip() for line in open('Unknowns.txt')])
=======
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open('eqns.txt')]
unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
edge_data = []
unknown = ''

listunkn = {}
#print unkn
#print eqns
>>>>>>> origin/merge

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

simu = []
=======
soln = 0
simu = []

>>>>>>> origin/merge
=======
soln = 0
simu = []

>>>>>>> origin/merge
=======
soln = 0
simu = []

>>>>>>> origin/merge
=======
soln = 0
simu = []

>>>>>>> origin/merge
Tarjan.reverse()

for curr in Tarjan:
    for now in curr:
        simu.append(eqns[now])
<<<<<<< HEAD
    soln = sy.solve(simu,unkns)
=======
    eqan = sy.sympify(simu)
    soln = sy.solve(eqan, unkns)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
    print soln

print Tarjan


#--------------------------------------------------------------------
# Drawing of Graph

pos = nx.spring_layout(G)
sypy = sy.sympify(eqns)
sol = sy.solve(sypy, unkns)

print sol

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos)
=======
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
=======
>>>>>>> origin/merge
nx.draw_networkx(G, pos)
nx.draw_networkx_edge_labels(G, pos)
#nx.draw_spring(G)
>>>>>>> origin/merge

plt.axis('off')
plt.show()
