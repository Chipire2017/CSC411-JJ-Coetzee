#2013-02-11

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

eqns = [line.strip() for line in open('eqns.txt')]
unkn = [line.strip() for line in open('Unknowns.txt')]
count_eqn = []
edge_data = []
unknown = ''
eqn = ''

#print unkn
#print eqns

for i in range(0,len(unkn)):
    for k in range(0,len(eqns)):
        count_eqn.append(k+1)   #Gives an Equation Number
        unk = unkn[i]
        eqn = eqns[k]
        if unk in eqn:
            edge = (str(k+1),unkn[i])
            edge_data.append(edge)

G = nx.DiGraph()
G.add_edges_from(edge_data)

Tarjan = nx.strongly_connected_components(G)
print Tarjan

pos = nx.random_layout(G)

#nx.draw_networkx_nodes(G,pos,node_size=700)
#nx.draw_networkx_edges(G,pos,edgelist = edge_data,width = 3)
#nx.draw_networkx_labels(G, pos,font_size=16,font_family='sans-serif')
nx.draw_random(G)


plt.axis('off')
#plt.savefig('Structure DiGraph')
plt.show()


