import networkx as nx
import sympy as sy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


def FindUnknowns(eqns):
    unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
    return unkns

def readeqns(filename):
    all_eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open(filename)]

    eqns = []
    inequ = {}
    for eq in all_eqns:
        if not isinstance(eq, tuple):
            eqns.append(eq)             #Create list of equations
        else:
            inequ[eq[1]] = eq[0]        #Put inequalities in dictionary

    unkns = FindUnknowns(eqns)
    return eqns, inequ, unkns

def InsertKnowns(known, eqns):
    
    for eq in eqns:
        for nm, val in known.iteritems():
            if nm in str(eq):
                i = eqns.index(eq)
                eq = eq.subs(nm, val)
                eqns[i] = eq
                
    unkns = FindUnknowns(eqns)
                 
    return eqns, unkns
    
def SortEquations(eqns):
    sorteq = []
    neweq = []    
    n = 1
    for eq in eqns:
        if not eq == 0:
            neweq.append(eq)
            
    while len(sorteq)<len(neweq):
        for eq in eqns:
            num_unkn = len(sorted(eqns[eqns.index(eq)].atoms(sy.Symbol)))
            
            if num_unkn == n: 
                sorteq.append(eq)
            
        n+=1
    
    return sorteq
    
def SequentialSolving(eqns):
    sorteq = SortEquations(eqns)
    #print sorteq
    seqsol = {}
    print sorteq
    unkn = sorted(sorteq[0].atoms(sy.Symbol))    
    num_unkn = len(unkn)
    while num_unkn == 1:
        #unkn = sorted(sorteq[0].atoms(sy.Symbol))
        print sorteq[0], unkn[0]
        val_unkn = sy.solve(sorteq[0], unkn[0])
        print unkn, val_unkn
        seqsol[unkn[0]] = val_unkn[0]
        i = 0
        for eq in sorteq:
            
            if unkn[0] in sorteq[i]:
                repl = eq.subs(unkn[0], sy.Rational(str(val_unkn[0])))
                sorteq[i] = repl
            i+=1 
        sorteq = SortEquations(sorteq)
        unkn = sorted(sorteq[0].atoms(sy.Symbol))
        num_unkn = len(unkn)
                
    return seqsol
    
def FindSubset(specV, eqns):
    subset = []
    for eq in eqns:
        for nm, val in specV.iteritems(): 
            if nm in str(eq):
                if len(sorted(eq.atoms(sy.Symbol)))>1:
#                if len(FindUnknowns(eq))>1:
#                    var = sy.Symbol(nm)
#                    eq = eq.subs(var, val) 
                    subset.append(eq)
    if len(subset)>0:
        subunkn = FindUnknowns(subset) 
    else:
        subunkn = [] 
    return subset, subunkn
    
def SolveSubset(subset, subeqns):
    subset = SortEquations(subset)
    seq_sol = SequentialSolving(subset)
    simu = {}
    for eq in subset:
        if eq == 0:
            subset.remove(eq)
    sim_eq = FindUnknowns(subset)
    simu = sy.solve(subset, sim_eq)
    
    sol = dict(seq_sol.items() + simu.items())
    
    return sol        
        
     
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
    Tjan = SortTarjan(Tjan, eqns, unkns)
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


def solvr(Tjan, eqns, unkns): 
     #Tjan = Tarjan(eqns, unkns)  
#    TjanSort = SortTarjan(Tjan, eqns, unkns)
#    print TjanSort
    
    simu = []
    sol = {}
    
    for curr in Tjan:
        if len(curr) == 1:
            for now in curr:
                tel = 0
                eq = eqns[now]
                var = sorted(eqns[now].atoms(sy.Symbol))   
                print now, eq, var                
                solv = sy.solve(eq, var)
                print solv
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
