import networkx as nx
import sympy as sy
import test_solver as ts
#from sympy import *
from sympy.parsing.sympy_parser import parse_expr

def readeqns(filename):
    all_eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open(filename)]

    eqns = []
    inequ = {}
    for eq in all_eqns:
        if not isinstance(eq, tuple):
            eqns.append(eq)             #Create list of equations
        else:
            inequ[eq[1]] = eq[0]        #Put inequalities in dictionary

    unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
    return eqns, inequ, unkns
    
def InsertKnowns(specV, cnst, eqns, unkns):

    print unkns
    for unkn in unkns:
        for nm, value in specV.iteritems():
            if nm == str(unkn):
                tel = 0
                for eq in eqns:
                    if nm in str(eq):
                        eq = eq.subs(nm, value)
                        eqns[tel] = eq
                        print unkns             
                    tel = tel + 1
                del unkns[unkns.index(unkn)]
        for ct, val in cnst.iteritems():
            if ct == str(unkn):
                tel = 0
                for eq in eqns:
                    if ct in str(eq):
                        eq = eq.subs(ct, val)
                        eqns[tel] = eq            
        
                    tel = tel + 1
        
    return eqns, unkns

    
def Tarjan(eqns, unkns):
    

    G = nx.DiGraph()

    for unkn in unkns:
        for curr_node in range(0,len(eqns)):
            if unkn in eqns[curr_node]:
                for next_node in range(curr_node,len(eqns)):
                    if unkn in eqns[next_node]:
                        if G.has_edge(curr_node,next_node):
                            G.add_edge(next_node,curr_node,label=str(unkn))
                        else:
                            G.add_edge(curr_node,next_node,label=str(unkn))

    Tjan = nx.strongly_connected_components(G)
    Tjan.reverse()
    
    return Tjan
    
def SortTarjan(Tjan, eqns, unkns):

    seq = []
    for curr in Tjan: 
        if len(curr) == 1:
            seq.append(curr[0])        
    for eq in seq:
        num_unk = len(sorted(eqns[eq].atoms(sy.Symbol)))
        for nxt_eq in range(eq,len(seq)):
            num_unk2 = len(sorted(eqns[nxt_eq].atoms(sy.Symbol)))
            if num_unk2 < num_unk:
                Tjan[nxt_eq], Tjan[eq] = Tjan[eq], Tjan[nxt_eq] 
                
                
                
            
    return Tjan


def solvr(eqns, unkns): 
    Tjan = Tarjan(eqns, unkns)  
    TjanSort = SortTarjan(Tjan, eqns, unkns)
    
    simu = []
    sol = {}
    
    for curr in TjanSort:
        if len(curr) == 1:
            for now in curr:
                tel = 0
                eq = eqns[now]
                var = sorted(eqns[now].atoms(sy.Symbol))   
                solv = sy.solve(eq, var)
                val = solv[0]
                for repl in eqns:    #Replace unknowns with values in equations
                    repl = repl.subs(var[0], val)
                    eqns[tel] = repl
                    tel +=1
                sol[var[0]] = val
        elif len(curr) > 1:
            tel = len(sol)
            for now in curr:
                simu.append(eqns[now])
                #mul_var.append(unkns[now])
            soln = sy.solve(simu, unkns)

            sol = dict(sol.items() + soln.items())
    for key in sol:
        sol[key] = float(sol.get(key))
        sol[key] = '%0.2f' % sol[key]
    return sol
    
    ts.TarjanTest
