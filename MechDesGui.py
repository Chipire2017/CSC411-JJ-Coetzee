# -*- coding:utf-8 -*-
"""
Created on 03 Apr 2011

@author: Administrator
"""
from __future__ import division
from Tkinter import *
from math import *
import numpy as np
#import eqtn
import solverc as sc

class Mainframe:
    def __init__(self, parent):
        self.myParent = parent

        self.dSpb = {}
        self.cbxVar = {}
        self.varCb = {}
        self.dScl = {}
        self.dCspb = {}

        # Read info about names and equations
        self.cnstnm = [line.strip() for line in open('cnstnm.txt')]
        self.incidence = np.loadtxt('base.txt')
        self.cnsts = [float(line.strip()) for line in open('const.txt')]
        self.eqns, self.inequ, self.unkns = sc.readeqns('eqns.txt')
        self.names = [line.strip() for line in open('Unknowns.txt')]
        self.dCnst = dict(zip(self.cnstnm, self.cnsts))
        #specced = {'Lo' : 11, 'mV' : 2300, 'V1' : 234, 'mL' : 12}

        ## Defining widgets

        # Frame holding everything
        self.mFrame = Frame(self.myParent)
        self.mFrame.grid()
        self.mFrame.pack()
        
        
        # Frame for tool bar
        self.frmTbar = Frame(self.mFrame)
        self.frmTbar.grid(row = 0, column = 0, sticky = E, pady = '0.2c', padx= '0.2c')
        
        # Frame for page tabs (to be implemented later)
        self.frmTabs = Frame(self.frmTbar)
        self.frmTabs.grid(row = 0, column = 0)
        # tb buttons
        self.btnSave = Button(self.frmTabs, text = "Save", command = self.sav) #  bind to udpent (update entry)
        self.btnSave.grid(row = 0, column = 0)
    
        # Frame for page tabs (to be implemented later)
        self.frtbpt = Frame(self.frmTbar)
        self.frtbpt.grid(row = 0, column = 1)
        # Page index buttons (tab).
        self.btnConstants = Button(self.frtbpt, text="Constants",command = self.dispc)
        self.btnConstants.grid(row = 0, column = 0)
        self.btnDisp1 = Button(self.frtbpt, text="Variables", command = self.disp1)        
        self.btnDisp1.grid(row = 0, column = 1)
        self.btnDisp2 = Button(self.frtbpt, text="2",command = self.disp2)
        self.btnDisp2.grid(row = 0, column = 2)
        self.btnDisp3 = Button(self.frtbpt, text="3",command = self.disp3)
        self.btnDisp3.grid(row = 0, column = 3)
        
        
    def ConstantsFrame(self):
        
        self.frmConst = Canvas(self.mFrame, scrollregion = (0,0,1024,768))
        self.btnConstSpec = Button(self.frmConst, text = "Constants Specified, Continue?", command = self.disp1)
        self.btnConstSpec.grid(columnspan = 3, rowspan = 2, sticky = N+S+W+E)
        self.lblCnstFSpec = Label(self.frmConst, text = "Constants fully specified", background = 'green')
        self.lblCnstNFSpec = Label(self.frmConst, text = " Constants have not been specified", background = 'red')
        self.lblCnstFSpec.grid(row = 2, columnspan = 3)
        self.btnCold = Button(self.frmConst, text = "Use original Values", command = self.btco)
        self.btnClear = Button(self.frmTabs, text = "Clear", command = self.ClearConstants)
        self.btnClear.grid(row = 0, column = 1)        
        mcol = 3
        rw = 3
        i = 0
        while (i < (len(self.cnstnm))):
            col = 0
            while (i < len(self.cnstnm)) and (col <= (mcol-1)):
                self.lblfrConst = LabelFrame(self.frmConst, text = self.cnstnm[i], labelanchor = 'nw')
    
                self.dCspb[self.cnstnm[i]] = Spinbox(self.lblfrConst, width = 6,from_ = 0,to=1000000, format = '%0.2f', increment = 0.01)
                self.dCspb[self.cnstnm[i]].delete(0, last=END)
                self.dCspb[self.cnstnm[i]].insert(0, self.dCnst[self.cnstnm[i]])
                self.dCspb[self.cnstnm[i]].grid(row = 0, column = 0, padx = '1c',pady = '0.2c')
                self.dCspb[self.cnstnm[i]].event_add ( "<<allcnst>>", "<Button-1>", "<KP_Enter>" ,"<FocusOut>","<Up>","<Down>")
                self.dCspb[self.cnstnm[i]].bind("<<allcnst>>", self.cnstok)
                self.lblIndConst = Label(self.lblfrConst, text = self.cnstnm[i]) #Will add units later
                self.lblIndConst.grid(row = 0, column = 1, padx = '1c')
    
                self.lblfrConst.grid(row = rw, column = col, sticky = W+E,pady = '0.3c', padx = '0.1c')
                i = i + 1
                col = col + 1
            rw = rw + 1
        self.frmConst.grid(row = 1, column = 0)
        
        
        
    def VariablesFrame(self):
       
        self.frmVar = Canvas(self.mFrame, scrollregion = (0,0,1024,768))
        self.btnSolve = Button(self.frmTabs, text = "Solve", state = DISABLED, command = self.SolveClick) #  bind to udpent (update entry)
        self.btnSolve.grid(row = 0, column = 1)
        self.btnClear = Button(self.frmTabs, text = "Clear", command = self.ClearVariables)
        self.btnClear.grid(row = 0, column = 2)

        # Frame showing number of DOF       
        self.frDOF = LabelFrame(self.frmVar, text = "DOF", labelanchor='nw')
        self.lblDOF = Label(self.frDOF, text= "DOF", padx=3, pady=3)
        self.lblDOF.grid()
        self.frDOF.grid(row=0, column=0, sticky='NW', padx='0.1c', pady='0.3c') 
        self.frmIndicator = {}
        # Place frame (label and edit) for each variable in names
        mcol = 8 # Maximum labelframes / column
        rownos = 1
        i = 0
        var = []
        while (i < (len(self.names))):
            colnos = 0
            while (i < len(self.names)) and (colnos <= (mcol-1)):
                # create a new frame for each iteration in the loop
                self.lfr = LabelFrame(self.frmVar, text = self.names[i], labelanchor = 'nw')
                
                self.frmIndicator[self.names[i]] = Frame(self.lfr, height = 3, width = 50)
                self.frmIndicator[self.names[i]].grid(row = 0, column = 0)
                self.dSpb[self.names[i]] = Spinbox(self.lfr, width = 5, from_ = 0, to = 100000, increment = 0.01, format = '%0.2f', state = "readonly")
                self.dSpb[self.names[i]].grid(row = 1, column = 0, sticky = N+S)
                #self.dSpb[self.names[i]].event_add ( "<<allspb>>", "<Button-1>", "<KP_Enter>" ,"<FocusIn>")
                #self.dSpb[self.names[i]].bind("<<allspb>>", self.sav)
                self.dSpb[self.names[i]].delete(0,last=END)
                self.dScl[self.names[i]] = Scale(self.lfr, orient=HORIZONTAL, length = '4c')
                self.dScl[self.names[i]].grid(row = 2, column = 0, sticky = N+S)
                var.append(IntVar())
                self.cbxVar[self.names[i]] = Checkbutton(self.lfr, text = None, onvalue = 1, variable = var[i], command = self.SelectVar)
                                
                self.varCb[self.names[i]] = var[i]     
                self.cbxVar[self.names[i]].grid(row = 1, column = 1)
                self.lfr.grid(row = rownos, column = colnos, sticky = W+E,pady = '0.3c', padx = '0.1c')
                
                i = i + 1
                colnos = colnos + 1
            rownos = rownos + 1
    
        self.scrollY = Scrollbar(self.frmVar,orient=VERTICAL, command = self.frmVar.yview )
        self.scrollY.grid (row = 0, rowspan = rownos, column=mcol+1, sticky=N+S+E )
        self.frmVar["yscrollcommand"] = self.scrollY.set
    

    def Frame1(self):
        
        self.frm1 = Canvas(self.mFrame, scrollregion = (0,0,1024,768))
        self.btnP1 = Button(self.frm1,text = "Page 1 Inactive")
        self.btnP1.grid(row = 1, column = 1, pady = '2c')
        self.lblResCost = Label(self.frm1, text = "Reserved Cost")
        self.lblResCost.grid(row = 1, column = 2, pady = '2c')
        
    def Frame2(self):
        
        self.frm2 = Canvas(self.mFrame, scrollregion = (0,0,1024,768))
        self.btnP2 = Button(self.frm2,text = "Page 2 Inactive")
        self.btnP2.grid(row = 1, column = 1, pady = '2c')
        self.lblResColDia = Label(self.frm2, text = "Reserved Column Diagram")
        self.lblResColDia.grid(row = 1, column = 2, pady = '2c')
        
    def Frame3(self):

        self.frm3 = Canvas(self.mFrame,scrollregion = (0,0,1500,900))
        self.btnP3 = Button(self.frm3,text = "Page 3 Inactive")
        self.btnP3.grid(row = 1, column = 1, pady = '2c')
        self.lblCostOpt = Label(self.frm3, text = "Reserved for Cost Optimisation")
        self.lblCostOpt.grid(row = 1, column = 2, pady = '2c')
                
    #Display relevant frame and remove the other (don't forget)
    def dispc(self):
        self.frmVar.grid_remove()
        self.frm2.grid_remove()
        self.frm3.grid_remove()
       # self.frm4.grid_remove()
        self.frmConst.grid(row = 1, column = 0)
            
    def disp1(self):
#        seq_eq = []        
        #print self.unkns
        #print self.dCnst
        self.eqns, self.unkns = sc.InsertKnowns(self.dCnst, self.eqns, self.unkns)
        initSol = sc.SequentialSolving(self.eqns) 
        print initSol
        for nm in self.dSpb.keys():
                for var in initSol:
                    if nm == str(var):
                        self.dSpb[nm].configure(state=NORMAL)
                        self.dSpb[nm].delete(0,last=END)
                        self.dSpb[nm].insert(0, initSol.get(var)) 
                        self.dSpb[nm].configure(state='readonly')
#        constTarjan = sc.Tarjan(self.eqns, self.unkns)
#        print constTarjan
#        for num in constTarjan:
#            print num, self.eqns[num[0]]
#            if len(num) == 1:
#                seq_eq.append(num)
#       
#        print seq_eq
#        sol = sc.solvr(seq_eq, self.eqns, self.unkns)
        
        self.frmConst.grid_remove()
        self.frm2.grid_remove()
        self.frm3.grid_remove()
        
        self.frmVar.grid(row =1, column = 0)
        
    
    def disp2(self):
        self.frmConst.grid_remove()
        self.frmVar.grid_remove()
        self.frm3.grid_remove()
        #self.frm4.grid_remove()
        self.frm2.grid(row =1, column = 0)
    
    def disp3(self):
        self.frmConst.grid_remove()
        self.frmVar.grid_remove()
        self.frm2.grid_remove()
        #self.frm4.grid_remove()
        self.frm3.grid(row =1, column = 0)
    
    # Function which takes updates entry widgets when variables become specified from mofifier
    def sav(self, event):
        return
        for nm in self.dSpb.keys():
            if self.dSpb[nm].get() <> '':
                self.specv[nm] = float(self.dSpb[nm].get())
                self.defV(self.specv, self.names, self.incidence, nm, float(self.dSpb[nm].get()))
        print specv
    
    # Clear whichever field is in view
    def ClearVariables(self):
        
        for vspb in dSpb.keys():
            self.dSpb[vspb].delete(0,last=END)
            self.dSpb[vspb].insert(0,'')
        self.sp.clear()
        self.specv.clear()
        
    def ClearConstants(self):
        for vcspb in self.dCspb.keys():
            self.dCspb[vcspb].delete(0,last=END)
            self.dCspb[vcspb].insert(0,'')
        self.dCnst.clear()     
       

    def cnstok(self, event):
        self.cnsts = [(self.dCspb[j].get()) for j in (self.cnstnm)]
        a = self.cnsts.count('')
        if a > 0:
            self.lblCnstNFSpec = Label(self.frmConst, text = str(a)+" Constant(s) NOT yet specified")
            self.lblCnstFSpec.grid_remove()
            self.lblCnstNFSpec.grid(row = 2, columnspan = 2, pady = '2c')
            self.btnCold.grid(row = 2, column = 2, pady = '2c')
        else:
            self.btnCold.grid_remove()
            self.lblCnstNFSpec.grid_remove()
            self.lblCnstFSpec.grid_remove()
            self.lblCnstFSpec.grid(row = 2, columnspan = 3, pady = '2c')
            for nmc in self.cnstnm:
                self.dCnst[nmc] = float(self.dCspb[nmc].get())
            print self.dCnst
       

    # Insert original constants, 
    def btco(self):
        [self.dCspb[nm].insert(0,self.cnsts[i]) for i, nm in enumerate(self.cnstnm)]
        self.btnCold.grid_remove()
        self.lblCnstNFSpec.grid_remove()
        self.lblCnstFSpec.grid_remove()
        self.lblCnstFSpec.grid(row = 2, columnspan = 3, pady = '2c')
    
        
    # calculate Degrees of freedom
    def DOF(self, eqns, unkns):
        DeOF = int(len(unkns)-len(eqns))
        return DeOF    
        
    # Define Click on Spinbox
    def NumFixVar(self):
        NumFixVar = 0;
        for nm in self.cbxVar:
            if (self.varCb.get(nm)).get():
                NumFixVar+=1
        return NumFixVar
            
    def SelectVar(self):   
        
        self.subunkn = {}
        self.specV = {}
        NumFix = self.NumFixVar()
        if NumFix == 0:
            self.lblDOF.config(text="Fix a Variable")
            self.lblDOF.update_idletasks() 
            self.subset = {}
            self.specV.clear()
            myColour = 'light grey'
            for nm in self.dSpb.keys():
                print nm
                self.dSpb[nm].config(state='readonly')
                self.frmIndicator[nm].config(bg=myColour)
        elif NumFix == 1:
            i = 0
            for nm in self.cbxVar:
                if (self.varCb.get(nm)).get():
                    self.dSpb[str(nm)].config(state=NORMAL)
                    self.frmIndicator[nm].config(bg='red')
                    self.specV[nm] = self.dSpb[nm].get()
                    self.fixedvar = nm
                else:
                    self.dSpb[str(nm)].config(state='readonly', background = None)
                i+=1
                
                
            self.subset, self.subunkn = sc.FindSubset(self.specV, self.eqns)
            for nm in self.dSpb.keys():
                for var in self.subunkn:   
                    if nm == str(var) and not nm == self.fixedvar:
                        self.frmIndicator[nm].config(bg='green')                    
            
            self.DeOF = self.DOF(self.subset, self.subunkn)
            print str(self.DeOF-1)
            self.lblDOF.config(text="Specify %s variables" %str(self.DeOF-1))
            self.lblDOF.update_idletasks()
            print self.subset
            print self.subunkn
            
        elif NumFix > 1:
            print self.subset
            var = []
            
            for eq in self.subset:
                var = sc.FindUnknowns(self.subset)
                if len(var) == 2 and not var[0] == self.fixedvar:
                    self.dSpb[str(var[0])].config(state='readonly')
                
                        
            while self.DeOF>0:        
                for nm in self.cbxVar:
                    if (self.varCb.get(nm)).get():
                        self.dSpb[str(nm)].config(state=NORMAL)
                        #self.specV[nm] = self.dSpb[nm].get()
                        self.DeOF=self.DeOF-1
                self.lblDOF.config(text="Specify %s variables" %str(self.DeOF-1))
                self.lblDOF.update_idletasks()        
                        
            if self.DeOF == 0:
                self.btnSolve.config(state=NORMAL)
            else:
                self.btnSolve.config(state=DISABLED)
       
    
    # Call solve
    def solv(self):
        for nm in self.dSpb.keys():
            if (self.varCb.get(nm)).get():
               self.specV[nm] = self.dSpb[nm].get() 
        
        print self.subset
        print 'DOF = ', self.DeOF
        print self.specV   
        self.subset, self.subunkn = sc.InsertKnowns(self.specV, self.subset, self.subunkn)
                 
        if self.DeOF == 0:
           self.sp = sc.SolveSubset(self.subset, self.subunkn) 
           for nm in self.dSpb.keys():
                for var in self.sp:
                    if nm == str(var):
                        self.dSpb[nm].config(state=NORMAL)
                        self.dSpb[nm].delete(0,last=END)
                        self.dSpb[nm].insert(0, self.sp.get(var))
           self.lblDOF.config(text="System fully specified")
           self.lblDOF.update_idletasks()
            
           print "Solve Ran to Competion"
        elif self.DeOF < 0:
           print "System overspecified"
           self.lblDOF.config(text="System overspecified")
           self.lblDOF.update_idletasks()
        
    # Define Solve Click event
    def SolveClick(self):
        self.solv()
        return
       
                       

def main():
    root = Tk()
    myApp = Mainframe(root)
    Mainframe.ConstantsFrame(myApp)
    Mainframe.VariablesFrame(myApp)
    Mainframe.Frame1(myApp)
    Mainframe.Frame2(myApp)
    Mainframe.Frame3(myApp)
    root.mainloop()
    
if __name__ == '__main__':
    main()
#root = Tk()
#root.title = "OMDDC"
#myApp = MechGui(root, "OMDDC")
#
#root.mainloop()


