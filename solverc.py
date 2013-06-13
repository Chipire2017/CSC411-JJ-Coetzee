
import sympy as sy
import csv
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


# Read Data From csv files
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
           
    return Name, Descript, Value, Units

#Find unknowns in an equation or equations
def FindUnknowns(eqns):
    
    if not isinstance(eqns, sy.Add) and not isinstance(eqns, Float):    
        if len(eqns)>1:        
            unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]
        elif len(eqns)==1:
            unkns = sorted(eqns[0].atoms(sy.Symbol))
    elif isinstance(eqns, sy.Add):
        unkns = sorted(eqns.atoms(sy.Symbol))
    if eqns == [] or isinstance(eqns, Float):
        unkns = []
    
    return unkns
#Read Equations from File
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

#Insert Known Variables into Equations
def InsertKnowns(known, eqns):
    inseq = eqns[:]
    if not known == {}:
        for eq in inseq:
            for nm, val in known.iteritems():
                if str(nm) in str(eq):
                    i = inseq.index(eq)
                    eq = eq.subs(nm, val)
                    inseq[i] = eq
                    
    unkns = FindUnknowns(inseq)
    inseq = RemoveZeros(inseq)             
    return inseq, unkns

#Remove zeroes from equations    
def RemoveZeros(eqns):
    neweq = []
    for eq in eqns:
        if not eq < 0.0001:
            neweq.append(eq)
    
    return neweq

#Sort equations from least amount of unknowns     
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

#Sequentially solves a system    
def SequentialSolving(eqns):
    sorteq = SortEquations(eqns)
    seqsol = {}
    unkn = sorted(sorteq[0].atoms(sy.Symbol)) 
    num_unkn = len(unkn)
    while num_unkn == 1 and not sorteq == []:  
        val_unkn = sy.solve(sorteq[0], unkn[0], simplify = False) 
        seqsol[unkn[0]] = sy.Rational(str(round(val_unkn[0], 4)))
    unkn = sorted(sorteq[0].atoms(sy.Symbol))    
    num_unkn = len(unkn)
    while num_unkn == 1:    
        val_unkn = sy.solve(sorteq[0], unkn[0])   
        seqsol[unkn[0]] = val_unkn[0]
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
                
    return seqsol

#Finds Subsystem of Equations     
def FindSubset(specV, eqns):
    subset = []
    for eq in eqns:
        for nm, val in specV.iteritems(): 
            if nm in str(eq):
                if len(sorted(eq.atoms(sy.Symbol)))>1:
                    subset.append(eq)
    if len(subset)>0:
        subunkn = FindUnknowns(subset) 
    else:
        subunkn = [] 
    return subset, subunkn

#Find Number of Equations with only one unknown    
def FindNumberOfSatisfiedEquations(eqns):
    num_satisfied = 0
    eqns_satisfied = []  
    for eq in eqns:
        unkn = FindUnknowns(eq)
        if len(unkn) == 1:
            num_satisfied +=1
            eqns_satisfied.append(eq)
    
    return num_satisfied, eqns_satisfied
    
# Used to solve subset of equations   
def SolveSubset(eqns, subset, subeqns, specV):
    neweq = eqns[:]   
    unkn = []
    soln = {}
    subset, unkn = InsertKnowns(specV, subset)
    init_sol = sy.solve(subset, unkn, simplify = False)   
    neweq, unkns = InsertKnowns(specV, neweq)

    num_satisfied, eq_satisfied = FindNumberOfSatisfiedEquations(neweq)
    while num_satisfied > 0:
        unkn_sat = FindUnknowns(eq_satisfied)
        solv = sy.solve(eq_satisfied, unkn_sat, simplify = False)
        soln.update(solv)
        neweq, unkns = InsertKnowns(soln, neweq)       
        num_satisfied, eq_satisfied = FindNumberOfSatisfiedEquations(neweq)

        if solv == []:
            num_satisfied = 0
            
    sol = dict(soln.items() + specV.items())# + init_sol.items()) 
    
    
    return sol        
