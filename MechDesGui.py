# -*- coding:utf-8 -*-
"""
Created on 24 May 2013

@author: Johan Coetzee
"""

from Tkinter import *
from math import *
import numpy as np
import solverc as sc
from PIL import ImageTk, Image

class Mainframe:
    def __init__(self, parent):
        self.myParent = parent

        self.dSpb = {}
        self.cbxVar = {}
        self.varCb = {}
        self.dScl = {}
        self.dCspb = {}

        # Read info about names and equations
        self.cnstnm, self.Cdescript, self.dCnst, self.Cunits = sc.NameParsing('cnstnm.csv')
        self.cnsts = [float(line.strip()) for line in open('const.txt')]
        self.eqns, self.inequ, self.unkns = sc.readeqns('equations.txt')
        self.names, self.Vdescript, self.Val, self.Vunits = sc.NameParsing('varn.csv')
        
        #specced = {'Lo' : 11, 'mV' : 2300, 'V1' : 234, 'mL' : 12}

        ## Defining widgets

        # Frame holding everything
        self.mFrame = Frame(self.myParent, height = 500, width = 1000)
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
        self.frmConstDiagram = LabelFrame(self.frmConst, text = 'Basic Distillation Column', labelanchor = 'nw')
        self.frmCDiagram = Canvas(self.frmConstDiagram, height = 200, width = 200)
        
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
                self.lblfrConst = LabelFrame(self.frmConst, text = self.Cdescript[i], labelanchor = 'nw')
    
                self.dCspb[self.cnstnm[i]] = Spinbox(self.lblfrConst, width = 6,from_ = 0,to=1000000, format = '%0.2f', increment = 0.01)
                self.dCspb[self.cnstnm[i]].delete(0, last=END)
                self.dCspb[self.cnstnm[i]].insert(0, self.dCnst[self.cnstnm[i]])
                self.dCspb[self.cnstnm[i]].grid(row = 0, column = 0, padx = '1c',pady = '0.2c')
                self.dCspb[self.cnstnm[i]].event_add ( "<<allcnst>>", "<Button-1>", "<KP_Enter>" ,"<FocusOut>","<Up>","<Down>")
                self.dCspb[self.cnstnm[i]].bind("<<allcnst>>", self.cnstok)
                self.lblIndConst = Label(self.lblfrConst, text = self.Cunits[i]) #Will add units later
                self.lblIndConst.grid(row = 0, column = 1, padx = '1c')
    
                self.lblfrConst.grid(row = rw, column = col, sticky = W+E,pady = '0.3c', padx = '0.1c')
                i = i + 1
                col = col + 1
            rw = rw + 1
        self.frmConst.grid(row = 1, column = 0, padx = '0.2c', pady = '0.2c')
        self.frmConstDiagram.grid(row = rw, column = 0)
        self.frmCDiagram.grid()
        self.ConstGrap = ImageTk.PhotoImage(Image.open('BasicDistColumn.png'))
        self.frmCDiagram.create_image(100, 100, image = self.ConstGrap)
        
        
        
    def VariablesFrame(self):
        self.specV = {}
        self.frmVarTab = Canvas(self.mFrame)
        self.frmInfo = Canvas(self.frmVarTab)
        self.frmInfo.grid(row=0, column=0)
        self.frmVar = Canvas(self.frmVarTab, scrollregion = (0,0,2500,1080))
        self.frmVar.grid(row = 1, column = 0)
        self.btnSolve = Button(self.frmTabs, text = "Solve", state = DISABLED, command = self.solv) #  bind to udpent (update entry)
        self.btnSolve.grid(row = 0, column = 1)
        self.btnClear = Button(self.frmTabs, text = "Clear", command = self.ClearVariables)
        self.btnClear.grid(row = 0, column = 2)
        # Frame showing number of DOF   
        self.frmSystem = LabelFrame(self.frmInfo, text = 'System Status', padx = '0.5c', pady = '0.5c')
        self.frmSystem.grid(row = 0, column = 1)
        self.frDOF = LabelFrame(self.frmInfo, text = "Subsystem Status", labelanchor='nw')
        self.lblDOF = Label(self.frDOF,text = 'Specify a variable', background = 'yellow', padx=3, pady=3)
        self.lblDOF.grid()
        self.frDOF.grid(row=0, column=0, padx='0.1c', pady='0.3c') 
        self.frmIndicator = {}
        
        self.frmExtDist = LabelFrame(self.frmInfo, text = 'Extended Distillation Column', labelanchor = 'nw')
        self.ExtDistGraph = Canvas(self.frmExtDist, height = 200, width = 200)
        self.frmTrayLayout = LabelFrame(self.frmInfo, text = 'Tray Layout', labelanchor = 'nw')
        self.TrayLayGraph = Canvas(self.frmTrayLayout, height = 200, width = 200)
        self.frmTrayHydr = LabelFrame(self.frmInfo, text = 'Tray Hydraulics', labelanchor = 'nw')
        self.TrayHydrGraph = Canvas(self.frmTrayHydr, height = 200, width = 200)
        # Place frame (label and edit) for each variable in names
        mcol = 6 # Maximum labelframes / column
        rownos = 1
        i = 0
        var = []
        while (i < (len(self.names))):
            colnos = 0
            while (i < len(self.names)) and (colnos <= (mcol-1)):
                # create a new frame for each iteration in the loop
                self.lfr = LabelFrame(self.frmVar, text = self.Vdescript[i] + ' ' + self.Vunits[i], labelanchor = 'nw')
                
                self.frmIndicator[self.names[i]] = Frame(self.lfr, height = 3, width = 50)
                self.frmIndicator[self.names[i]].grid(row = 0, column = 0)
                self.dSpb[self.names[i]] = Spinbox(self.lfr, width = 5, from_ = -100000, to = 100000, increment = 0.1)
                self.dSpb[self.names[i]].grid(row = 1, column = 0, sticky = N+S)
#                self.lblIndVar = Label(self.lfr, text = self.Vunits[i]) #Will add units later
#                self.lblIndVar.grid(row = 0, column = 1, padx = '1c')
                #self.dSpb[self.names[i]].event_add ( "<<allspb>>", "<Button-1>", "<KP_Enter>" ,"<FocusIn>")
                self.dSpb[self.names[i]].bind("<Return>", self.SolveEnterPress)
                self.dSpb[self.names[i]].delete(0,last=END)
                self.dScl[self.names[i]] = Scale(self.lfr, orient=HORIZONTAL, length = '2c')
                self.dScl[self.names[i]].grid(row = 2, column = 0, sticky = N+S)
                var.append(IntVar())
                self.cbxVar[self.names[i]] = Checkbutton(self.lfr, text = None, onvalue = 1, variable = var[i], command = self.SelectVar)
                                
                self.varCb[self.names[i]] = var[i]     
                self.cbxVar[self.names[i]].grid(row = 1, column = 1)
                self.lfr.grid(row = rownos, column = colnos, sticky = W+E,pady = '0.3c', padx = '0.1c')
                
                i = i + 1
                colnos = colnos + 1
            rownos = rownos + 1
        
        self.frmExtDist.grid(row = 0, column = 2, padx = '0.2c', pady = '0.2c')
        self.frmTrayLayout.grid(row = 0, column = 3, padx = '0.2c', pady = '0.2c')
        self.frmTrayHydr.grid(row = 0, column = 4, padx = '0.2c', pady = '0.2c')
                
        self.ExtDistGraph.grid()
        self.TrayLayGraph.grid()
        self.TrayHydrGraph.grid()
        
        self.ExtDistImage = ImageTk.PhotoImage(Image.open('Extended Dist Column.png'))
        self.ExtDistGraph.create_image(100, 100, image = self.ExtDistImage)
        
        self.TrayLayImage = ImageTk.PhotoImage(Image.open('Tray Layout.png'))
        self.TrayLayGraph.create_image(100, 100, image = self.TrayLayImage)
        
        self.TrayHydrImage = ImageTk.PhotoImage(Image.open('Tray Hydraulics.png'))
        self.TrayHydrGraph.create_image(100, 100, image = self.TrayHydrImage)
        
        
        self.mFrame.update_idletasks()
        self.scrollY = Scrollbar(self.frmVar,orient=VERTICAL)
        self.scrollY.grid (row = 0, rowspan = rownos, column=mcol+1, sticky=N+S+E )
        self.frmVar.config(yscrollcommand=self.scrollY.set)
        self.scrollY.config(command = self.frmVar.yview)
        

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
        
        self.eqns, self.unkns = sc.InsertKnowns(self.dCnst, self.eqns)
        initSol = sc.SequentialSolving(self.eqns) 
        print initSol
        for nm in self.dSpb.keys():
#            self.dSpb[nm].configure(state=NORMAL)
#            self.dSpb[nm].delete(0,last=END)
#            self.dSpb[nm].insert(0, '')
#            self.dSpb[nm].configure(state='readonly')
            for var in initSol:
                if nm == str(var):
                    self.dSpb[nm].delete(0,last=END)
                    self.dSpb[nm].insert(0, str(round(float(initSol.get(var)), 2)))
    
        self.frmConst.grid_remove()
        self.frm2.grid_remove()
        self.frm3.grid_remove()
        
        self.frmVarTab.grid(row =1, column = 0, columnspan = 1)
        
    
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
        
        for vspb in self.dSpb.keys():
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
           
        self.NumFix = self.NumFixVar()
        print 'NumFix', self.NumFix 
        print self.NumFix
        if self.NumFix == 0:
            self.lblDOF.config(text="Fix a Variable", background = 'yellow')
            self.lblDOF.update_idletasks() 
            self.subset = {}
            self.subunkn = {}
            
            self.specV.clear()
            myColour = 'light grey'
            for nm in self.dSpb.keys():
                self.frmIndicator[nm].config(bg=myColour)
                self.cbxVar[nm].config(state = ACTIVE)
                
        elif self.NumFix == 1:    
            for nm in self.cbxVar:
                i = 0
                if (self.varCb.get(nm)).get():
                    self.frmIndicator[nm].config(bg='blue')
                    self.specV[nm] = self.dSpb[nm].get()
                    self.fixedvar = nm
                else:
                    self.cbxVar[nm].config(state=DISABLED)
                i+=1
            print 'specV', self.specV
            self.subset, self.subunkn = sc.FindSubset(self.specV, self.eqns)            
            for nm in self.dSpb.keys():
                for var in self.subunkn:   
                    if nm == str(var) and not nm == self.fixedvar:
                        self.frmIndicator[nm].config(bg='green') 
                        self.cbxVar[str(nm)].config(state = ACTIVE)
            
            # Check which equations are satisfied by the fixed variable            
            known = {}
            known[self.fixedvar] = float(self.dSpb[self.fixedvar].get())
            eqns, unkns = sc.InsertKnowns(known, self.subset)
            print 'eqns', eqns
            eqns = sc.SortEquations(eqns)
            for eq in eqns:
                unkn = sc.FindUnknowns(eq)
                if len(unkn) == 1:
                    self.cbxVar[str(unkn[0])].config(state=DISABLED)
                    self.frmIndicator[str(unkn[0])].config(bg = 'orange')                                
                                
                            
                        
            self.DeOF = self.DOF(self.subset, self.subunkn)-1
            print str(self.DeOF-1)
            self.lblDOF.config(text="Specify %s variables" %str(self.DeOF), background = 'yellow')
            self.lblDOF.update_idletasks()
            print self.subset
            print self.subunkn
            print 'DoF 1= ', self.DeOF
            if self.DeOF == 0:
                self.btnSolve.config(state=NORMAL)
                self.lblDOF.config(text="System Specified", background = 'green')
                self.solv()
            
                
          
        elif self.NumFix > 0:
            self.DeOF = self.DOF(self.subset, self.subunkn)-1
            for eq in self.subset:
                sub, var = sc.InsertKnowns({self.fixedvar : 0}, [eq])
                DOF = self.DOF(sub, var)
                if DOF == 1:
                    if (self.varCb.get(str(var[0]))).get():
                        
                        self.cbxVar[str(var[1])].config(state=DISABLED)
                        self.cbxVar[str(var[0])].config(state=ACTIVE)
                        self.frmIndicator[str(var[1])].config(bg = 'orange')
                        self.frmIndicator[str(var[0])].config(bg = 'green')
                    elif (self.varCb.get(str(var[1]))).get():
                        self.cbxVar[str(var[0])].config(state=DISABLED)
                        self.cbxVar[str(var[1])].config(state=ACTIVE)
                        self.frmIndicator[str(var[0])].config(bg = 'orange')
                        self.frmIndicator[str(var[1])].config(bg = 'green')
                    
                
            self.DeOF=self.DeOF-self.NumFix+1  #+1 Due to Specified variable in system
                   
            print 'DOF2=',self.DeOF            
            if self.DeOF == 0:
                self.btnSolve.config(state=NORMAL)
                self.lblDOF.config(text="System Specified", background = 'green')
                self.solv()
                
                self.lblDOF.config(text="Fix a Variable", background = 'yellow')
                self.lblDOF.update_idletasks() 
                self.subset = {}
                self.subunkn = {}
                
                self.specV.clear()
                myColour = 'light grey'
                for nm in self.dSpb.keys():
                    self.frmIndicator[nm].config(bg=myColour)
                    self.cbxVar[nm].config(state = ACTIVE)
                    self.NumFix = 0
            elif self.DeOF>0:
                self.btnSolve.config(state=DISABLED)
                self.lblDOF.config(text="Specify %s variables" %str(self.DeOF), background = 'yellow')
            else:
                self.btnSolve.config(state=DISABLED)
                self.lblDOF.config(text="System overspecified", background = 'red')
                
            
                
                
  # Call solve
    def solv(self):
        eqns = self.eqns
        for nm in self.dSpb.keys():
            if (self.varCb.get(nm)).get():
               self.specV[nm] = self.dSpb[nm].get() 
        
        print self.specV   
        subset, subunkn = sc.InsertKnowns(self.specV, self.subset)
        if self.DeOF == 0:
            self.sp = sc.SolveSubset(eqns, subset, subunkn, self.specV) 
            for nm in self.dSpb.keys():
                for var in self.sp:
                    if nm == str(var):
                        self.dSpb[nm].config(state=NORMAL)
                        self.dSpb[nm].delete(0,last=END)
                        self.dSpb[nm].insert(0, str(round(float(self.sp.get(var)), 2)))
            
            print "Solve Ran to Competion"
        elif self.DeOF < 0:
            print "System overspecified"   
            
    # Define Solve Click event
    def SolveEnterPress(self, event):
        if self.DeOF == 0:        
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


