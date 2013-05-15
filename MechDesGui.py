# -*- coding:utf-8 -*-
"""
Created on 03 Apr 2011

@author: Administrator
"""
from __future__ import division
from Tkinter import *
from math import *
import numpy as np
import eqtn
import solverc as sc

class Mainframe:
    def __init__(self, parent):
        self.myParent = parent

        self.dSpb = {}
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
        
        self.frmConst = Canvas(self.mFrame,scrollregion = (0,0,1024,768))
        self.frm1 = Canvas(self.mFrame, scrollregion = (0,0,1024,768))
        self.frm2 = Canvas(self.mFrame, scrollregion = (0,0,1024,768))
        self.frm3 = Canvas(self.mFrame,scrollregion = (0,0,5000,900))
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
                
        #Display relevant frame and remove the other (don't forget)
    def dispc(self):
        self.frm1.grid_remove()
        self.frm2.grid_remove()
        self.frm3.grid_remove()
       # self.frm4.grid_remove()
        self.frmConst.grid(row = 1, column = 0)
            
    def disp1(self):
        self.frmConst.grid_remove()
        self.frm2.grid_remove()
        self.frm3.grid_remove()
        
        self.frm1.grid(row =1, column = 0)
    
    def disp2(self):
        self.frmConst.grid_remove()
        self.frm1.grid_remove()
        self.frm3.grid_remove()
        #self.frm4.grid_remove()
        self.frm2.grid(row =1, column = 0)
    
    def disp3(self):
        self.frmConst.grid_remove()
        self.frm1.grid_remove()
        self.frm2.grid_remove()
        #self.frm4.grid_remove()
        self.frm3.grid(row =1, column = 0)
    
    # Function which takes updates entry widgets when variables become specified from mofifier
    def sav(self):
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

class ConstantsFrame(Mainframe):
    
    def __init__(self, parent):
        self.myParent = parent
        Mainframe.__init__(self, self.myParent)

        # Frame for all the small variable frames
        
        self.btnConstSpec = Button(self.frmConst, text = "Constants Specified, Continue?", command = self.disp1)
        self.btnConstSpec.grid(columnspan =3, rowspan = 2, sticky = N+S+W+E)
        self.lblCnstFSpec = Label(self.frmConst, text = "Constants fully specified")
        self.lblCnstNFSpec = Label(self.frmConst, text = " Constants have not been specified")
        self.lblCnstFSpec.grid(row = 2, columnspan = 3, pady = '2c')
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
                self.dCspb[self.cnstnm[i]].delete(0,last=END)
                self.dCspb[self.cnstnm[i]].insert(0,self.dCnst[self.cnstnm[i]])
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

        # Check if constants entered and update if changed
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
        self.cnsts = np.loadtxt('const.txt')
        [self.dCspb[nm].insert(0,self.cnsts[i]) for i, nm in enumerate(self.cnstnm)]
        self.btnCold.grid_remove()
        self.lblCnstNFSpec.grid_remove()
        self.lblCnstFSpec.grid_remove()
        self.lblCnstFSpec.grid(row = 2, columnspan = 3, pady = '2c')
    
    
    
    # Frame 1 - main form with all variables
class VariablesFrame(Mainframe):
        
    def __init__(self, parent):
        self.myParent = parent
        Mainframe.__init__(self, self.myParent)

        mcol = 8 # Maximum labelframes / column
    
        # Frame for each labelframes
        
       
        # Frame showing number of DOF
        self.btnSolve = Button(self.frmTabs, text = "Solve", command = self.SolveClick) #  bind to udpent (update entry)
        self.btnSolve.grid(row = 1, column = 1)
        self.btnClear = Button(self.frmTabs, text = "Clear", command = self.ClearVariables)
        self.btnClear.grid(row = 1, column = 2)
        self.frDOF = LabelFrame(self.frm1, text = "DOF", labelanchor='nw')
        
        self.lblDOF = Label(self.frDOF, text= "DOF", padx=3, pady=3)
        self.lblDOF.grid()
        self.frDOF.grid(row=0, column=0, sticky='NW', padx='0.1c', pady='0.3c') 
        
        # Place frame (label and edit) for each variable in names
        rownos = 1
        i = 0
        while (i < (len(self.names))):
            colnos = 0
            while (i < len(self.names)) and (colnos <= (mcol-1)):
                # create a new frame for each iteration in the loop
                self.lfr = LabelFrame(self.frm1, text = self.names[i], labelanchor = 'nw')
    
                self.dSpb[self.names[i]] = Spinbox(self.lfr, width = 5, from_ = -100000, to = 100000, increment = 0.01, format = '%0.2f')
                self.dSpb[self.names[i]].grid()
                self.dSpb[self.names[i]].event_add ( "<<allspb>>", "<Button-1>", "<KP_Enter>" ,"<FocusIn>")
                self.dSpb[self.names[i]].bind("<<allspb>>", self.sav)
                self.dSpb[self.names[i]].bind("<Button-1>", self.dSpbClick)
                self.dSpb[self.names[i]].bind("<FocusIn>", self.dSpbClick)
                self.dSpb[self.names[i]].delete(0,last=END)
                self.dScl[self.names[i]] = Scale(self.lfr,orient=HORIZONTAL,length = '4c')
                self.dScl[self.names[i]].grid()
                self.lfr.grid(row = rownos, column = colnos, sticky = W+E,pady = '0.3c', padx = '0.1c')
                
                i = i + 1
                colnos = colnos + 1
            rownos = rownos + 1
    
        self.scrollY = Scrollbar(self.frm1,orient=VERTICAL, command = self.frm1.yview )
        self.scrollY.grid (row = 0, rowspan = rownos, column=mcol+1, sticky=N+S+E )
        self.frm1["yscrollcommand"] = self.scrollY.set
        
    # calculate Degrees of freedom
    def DOF(self, eqns, unkns):
        DeOF = int(len(unkns)-len(eqns))
        return DeOF    
        
    # Define Click on Spinbox
    def dSpbClick(self, event):    
        DeOF = self.DOF(self.eqns, self.unkns)
        
        self.lblDOF.config(text="Specify %s variables" %str(DeOF))
        self.lblDOF.update_idletasks()
        
    # Call solve
    def solv(self): 
        specv = {}
        print self.eqns, self.unkns
        DeOF = self.DOF(self.eqns, self.unkns)
        print 'DOF is', DeOF
        while DeOF > 0:
    #        curr_spb = 
    #       specv[curr_spb] = float((dSpb[curr_spb].get()))
            for nm in self.dSpb.keys():
               if self.dSpb[nm].get() <> '':
                    specv[nm] = float((self.dSpb[nm].get()))
            print specv
            self.new_eqns, self.new_unkns = sc.InsertKnowns(specv, self.dCnst, self.eqns, self.unkns)
            DeOF = self.DOF(self.new_eqns, self.new_unkns)
            self.lblDOF.config(text="Specify %s variables" %str(DeOF+1))
            self.lblDOF.update_idletasks()
        specv.clear() 
        if DeOF == 0:
            
            self.sp = sc.solvr(self.new_eqns, self.new_unkns)
            print self.sp
            for nm in self.dSpb.keys():
                for var in self.sp:
                    if nm == str(var):
                        self.dSpb[nm].delete(0,last=END)
                        self.dSpb[nm].insert(0, self.sp.get(var)) 
            
            self.lblDOF.config(text="System fully specified")
            self.lblDOF.update_idletasks()
            
            print "Solve Ran to Competion"
        else:
            print "System overspecified"
        
       # print 'eqns now is', self.new_eqns, self.DeOF
        
    # Define Solve Click event
    def SolveClick(self):
        self.solv()
        return
       
class frame2(Mainframe):
    
    def __init__(self, parent):

        self.myParent = parent
        Mainframe.__init__(self, self.myParent)

        
        
        self.btnP2 = Button(self.frm2,text = "Page 2 Inactive")
        self.btnP2.grid(row = 1, column = 1, pady = '2c')
        self.lblResCost = Label(self.frm2, text = "Reserved Cost")
        self.lblResCost.grid(row = 1, column = 2, pady = '2c')
class frame3(Mainframe):
    
    def __init__(self, parent):
        self.myParent = parent
        Mainframe.__init__(self, self.myParent)

        # Frame for all the small variable frames
       
        self.btnP3 = Button(self.frm3,text = "Page 3 Inactive")
        self.btnP3.grid(row = 1, column = 1, pady = '2c')
        self.lblResColDia = Label(self.frm3, text = "Reserved Column Diagram")
        self.lblResColDia.grid(row = 1, column = 2, pady = '2c')
    
class frame4(Mainframe):
    
    def __init__(self, parent):
        self.myParent = parent
        Mainframe.__init__(self)

        # Frame for all the small variable frames
        self.frm4 = Canvas(self.mFrame,scrollregion = (0,0,1500,900))
        self.btnP4 = Button(self.frm4,text = "Page 4 Inactive")
        self.btnP4.grid(row = 1, column = 1, pady = '2c')
        self.lblCostOpt = Label(self.frm4, text = "Reserved for Cost Optimisation")
        self.lblCostOpt.grid(row = 1, column = 2, pady = '2c')
    
                       

def main():
    root = Tk()
    myApp = Mainframe(root)
    ConstantsFrame(root)
    VariablesFrame(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
#root = Tk()
#root.title = "OMDDC"
#myApp = MechGui(root, "OMDDC")
#
#root.mainloop()


