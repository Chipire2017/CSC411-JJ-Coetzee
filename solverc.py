import networkx as nx
import sympy as sy
import csv
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from math import pi



def NameParsing(filename):
    
    Name = []
    Val = []
    Descript = []
    Units = []
    Value = {}
    contain  = open(filename, "rb")
    reader = csv.reader(contain)
    
    for row in reader:
        # Save header row.
        Name.append(row[0])
        Descript.append(row[1])
        Val.append(row[2])
        Units.append(row[3])
    contain.close() 
    
    for nm in Name:
        index =Name.index(nm)
        Value[nm] = Val[index]
        
    print Name    
    return Name, Descript, Value, Units

def FindUnknowns(eqns):
    if not isinstance(eqns, sy.Add) :    
        if len(eqns)>1:        
            unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
        elif len(eqns)==1:
            unkns = sorted(eqns[0].atoms(sy.Symbol))
    elif isinstance(eqns, sy.Add):
        unkns = sorted(eqns.atoms(sy.Symbol))
    if eqns == []:
        unkns = []
    
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
            if str(nm) in str(eq):
                i = eqns.index(eq)
                eq = eq.subs(nm, val)
                eqns[i] = eq
                
    unkns = FindUnknowns(eqns)
    eqns = RemoveZeros(eqns)             
    return eqns, unkns
    
def RemoveZeros(eqns):
    neweq = []
    for eq in eqns:
        if not eq < 0.0001:
            neweq.append(eq)
    
    return neweq
    
def SortEquations(eqns):
    sorteq = []
    neweq = []    
    n = 1
    for eq in eqns:
        if not eq < 0.0001:
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
    seqsol = {}
    unkn = sorted(sorteq[0].atoms(sy.Symbol)) 
    num_unkn = len(unkn)
    while num_unkn == 1 and not sorteq == []:   
        val_unkn = sy.solve(sorteq[0], unkn[0]) 
        print val_unkn
        seqsol[unkn[0]] = sy.Rational(str(round(val_unkn[0], 4)))
        print seqsol
        i = 0
        for eq in sorteq:
            if unkn[0] in sorteq[i]:    
                val_unkn[0] = round(val_unkn[0], 5)    
                repl = eq.subs(unkn[0], sy.Rational(str(val_unkn[0])))
                if not isinstance(repl, sy.Float):
                    sorteq[i] = repl
                else:
                    sorteq[i] = repl
            i+=1 
        
        sorteq = RemoveZeros(sorteq)
        if sorteq == []:
            num_unkn = 0
        else:
            sorteq = SortEquations(sorteq)
            unkn = sorted(sorteq[0].atoms(sy.Symbol))
            num_unkn = len(unkn)
    
    print 'seqsol', seqsol                
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
    
def FindNumberOfSatisfiedEquations(eqns):
    num_satisfied = 0
    eqns_satisfied = []    
    for eq in eqns:
        unkn = FindUnknowns(eq)
        if len(unkn) == 1:
            num_satisfied +=1
            eqns_satisfied.append(eq)
    
    return num_satisfied, eqns_satisfied
    
def SolveSubset(eqns, subset, subeqns, specV):
       
    print 'wat de teef', subset
    unkn = []
    subset = SortEquations(subset)
    print subset
    seq_sol = SequentialSolving(subset)
    print 'wat de teef 1', seq_sol
    subset, unkn = InsertKnowns(seq_sol, subset)    
    simu = {}
    soln = {}
    tel = 1
    newsubs = []
    
    for eq in subset:
        if not eq < 0.00001:
            eqns.append(eq)
            num_unkn = len(FindUnknowns(eq))
        else:
            num_unkn = 0
                 
        if num_unkn == 1:
            subset.remove(eq)
        tel +=1    
    if not newsubs == []:    
        sim_eq = FindUnknowns(newsubs)
        simu = sy.solve(newsubs, sim_eq)
    init_sol = dict(seq_sol.items() + simu.items() + specV.items())
    eqns, unkns = InsertKnowns(specV, eqns)
    eqns = SortEquations(eqns)
    num_satisfied, eq_satisfied = FindNumberOfSatisfiedEquations(eqns)
    print num_satisfied, eq_satisfied
    while num_satisfied > 0:
        #unkn_sat = FindUnknowns(eq_satisfied)
        soln.update(SequentialSolving(eq_satisfied))  
        eqns, unkns = InsertKnowns(soln, eqns)
        eqns = SortEquations(eqns)        
        num_satisfied, eq_satisfied = FindNumberOfSatisfiedEquations(eqns)
    sol = dict(init_sol.items() + soln.items()) 
    
    print 'sol', sol
    
    return sol        