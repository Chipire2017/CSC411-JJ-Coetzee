#2013-02-11
#2013-02-16

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import sympy as sy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


#-------------------------------------------------------------------------
# Extraction of Equations and Graph Creation
eqns = [line.strip() for line in open('eqns.txt')]
unkn = symbols([line.strip() for line in open('Unknowns.txt')])
eqn_numbering = {}
edge_data = []
unknown = ''
eqn = ''
listunkn = {}
#print unkn
#print eqns

G = nx.MultiDiGraph()

for i in range(0,len(unkn)):
    for k in range(0,len(eqns)):
        eqn_numbering[k+1] = eqns[k]
        eqn = sy.parsing.sympy_parser.parse_expr(eqns[k])
        listunkn[k+1] = str(eqn(k).args)
        if unkn[i] in eqn:
            curr_node = k+1
            for j in range(k+1,len(eqns)):
                eqn2 = sy.parsing.sympy_parser.parse_expr(eqns[j]) 
                if unkn[i] in eqn2:
                    next_node = j+1
                    if G.has_edge(curr_node,next_node):
                        G.add_edge(next_node,curr_node,weight=1,label=str(unkn[i]))
                    else:
                        G.add_edge(curr_node,next_node,weight=0.5,label=str(unkn[i]))


#-------------------------------------------------------------------
# Tarjan Algorithm and Symbolic Solving of Equations

Tarjan = nx.strongly_connected_components(G)
x = 0
soln =0
simu = []
teller = 0
Tarjan.reverse()
eqan = []

for i in range(0,len(Tarjan)):
    curr = Tarjan[i]
    if len(curr) == 1:
        now = curr[0]
        curr_eqn = eqn_numbering.get(curr[0])       
        eqan = sy.sympify(curr_eqn)
        soln = sy.solve(eqan,unkn)
        
    elif len(curr) > 1:
        for k in range(0,len(curr)):
            now = curr[k]
            simu.append(eqn_numbering.get(now)) 
        eqan = sy.sympify(simu)
        soln = sy.solve(eqan,unkn)
    print soln

print Tarjan
print listunkn

#--------------------------------------------------------------------
# Drawing of Graph

pos = nx.spring_layout(G)
sypy = sy.sympify(eqns)
sol = sy.solve(sypy,unkn)

print sol

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos)
#nx.draw_spring(G)

plt.axis('off')
#plt.savefig('Structure DiGraph')
plt.show()


