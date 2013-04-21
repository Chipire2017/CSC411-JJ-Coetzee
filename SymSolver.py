import matplotlib.pyplot as plt
import networkx as nx
import sympy as sy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


#-------------------------------------------------------------------------
# Extraction of Equations and Graph Creation
all_eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open('eqns.txt')]


eqns = []
inequ = {}
for eq in all_eqns:
    if not isinstance(eq, tuple):
        eqns.append(eq)             #Create list of equations
    else:
        inequ[eq[1]] = eq[0]        #Put inequalities in dictionary
        print inequ
        
unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
         
specV = {'p' : 2}

for unkn in unkns:
        for nm, value in specV.iteritems():
            if nm == str(unkn):
                tel = 0
                for eq in eqns:  
                    if nm in str(eq):
                        eq = eq.subs(nm, value)
                        eqns[tel] = eq
                    tel = tel + 1
                        

print eqns
print ' '

G = nx.DiGraph()


for unkn in unkns:
    for curr_node in range(0,len(eqns)):    
        if unkn in eqns[curr_node]:
            for next_node in range(curr_node,len(eqns)):
                if unkn in eqns[next_node]:
                    if G.has_edge(curr_node, next_node):
                        G.add_edge(next_node, curr_node, label = unkn)
                    else:
                        G.add_edge(curr_node, next_node, label = unkn)


#-------------------------------------------------------------------
# Tarjan Algorithm and Symbolic Solving of Equations

Tarjan = nx.strongly_connected_components(G)
simu = []
sol = {}
Tarjan.reverse()
print Tarjan
mul_var = []

for curr in Tarjan:
    if len(curr) == 1:
        for now in curr:
            tel = 0
            eq = eqns[now]
            var = unkns[now]     #Find current unknown - not robust at all
            solv = solve(eq, var)
            val = solv[0]
            for repl in eqns:    #Replace unknowns with values in equations
                repl = repl.subs(var, val)
                eqns[tel] = repl
                tel +=1
            sol[var] = solv[0]
    elif len(curr) > 1:
        tel = len(sol)
        for now in curr:
            simu.append(eqns[now])
            #mul_var.append(unkns[now])
        soln = sy.solve(simu, unkns)
        
        sol = dict(sol.items() + soln.items())
print sol



#--------------------------------------------------------------------
# Drawing of Graph

pos = nx.spring_layout(G)
sypy = sy.sympify(eqns)
sol = sy.solve(sypy,unkns)

print sol

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos)

plt.axis('off')
plt.show()


