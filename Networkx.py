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


eqns = [line.strip() for line in open('eqns.txt')]
unkn = symbols([line.strip() for line in open('Unknowns.txt')])
count_eqn = []
edge_data = []
unknown = ''
eqn = ''
listunkn = {}
#print unkn
#print eqns

for i in range(0,len(unkn)):
    for k in range(0,len(eqns)):
        count_eqn.append(k+1)   #Gives an Equation Number
        eqn = sy.parsing.sympy_parser.parse_expr(eqns[k])
        listunkn[k+1] = str(eqn(k).args)
        if unkn[i] in eqn:
            edge = (unkn[i],str(k+1))
            edge_data.append(edge)
            #edge = (str(k+1),unkn[i])
            #edge_data.append(edge)

G = nx.DiGraph()
G.add_edges_from(edge_data)
nx.write_gml(G, 'network.gml')

Tarjan = nx.strongly_connected_components(G)
print Tarjan
print listunkn

pos = nx.random_layout(G)
sol = sy.solve(eqns)

#nx.draw_networkx_nodes(G,pos,node_size=700)
#nx.draw_networkx_edges(G,pos,edgelist = edge_data,width = 3)
#nx.draw_networkx_labels(G, pos,font_size=16,font_family='sans-serif')
nx.draw_spring(G)


plt.axis('off')
#plt.savefig('Structure DiGraph')
plt.show()


