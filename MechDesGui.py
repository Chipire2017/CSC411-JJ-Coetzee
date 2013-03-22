# -*- coding:utf-8 -*-
"""
Created on 03 Apr 2011

@author: Administrator
"""
from __future__ import division
from Tkinter import *
import csv
from math import *
import numpy as np
import itertools
import eqtn
import solverc as sc

#Initialize dictionaries (use throughout module)
dFr = {}
dScl = {}
dSpb = {}
dCspb = {}
dvar = {}
specv = {}
sp = {}
dBtn = {}
dvar['crnt'] = 'frc'

# Read info about names and equations
names = [line.strip() for line in open('Unknowns.txt')]
cnstnm = [line.strip() for line in open('cnstnm.txt')]
incidence = np.loadtxt('base.txt')
cnsts = [float(line.strip()) for line in open('const.txt')]
eqns = [line.strip() for line in open('eqns.txt')]
dCnst = dict(zip(cnstnm,cnsts))
#specced = {'Lo' : 11, 'mV' : 2300, 'V1' : 234, 'mL' : 12}

# Function to create widgets
def createWidgets(form,names):

    # Frame holding everything
    dFr['fr'] = Frame(form)
    dFr['fr'].grid()

    # Frame for tool bar
    frtb = Frame(dFr['fr'])
    frtb.grid(row = 0, column = 0, sticky = E, pady = '0.2c', padx= '0.2c')

    # Frame for page tabs (to be implemented later)
    frtbb = Frame(frtb)
    frtbb.grid(row = 0, column = 0)
    # tb buttons
    bproc = Button(frtbb, text = "Save", command = sav) #  bind to udpent (update entry)
    bproc.grid(row = 0, column = 0)
    bsol = Button(frtbb, text = "Solve", command = solv) #  bind to udpent (update entry)
    bsol.grid(row = 0, column = 1)
    bclr = Button(frtbb, text = "Clear", command = clrspb)
    bclr.grid(row = 0, column = 2)


    # Frame for page tabs (to be implemented later)
    frtbpt = Frame(frtb)
    frtbpt.grid(row = 0, column = 1)
    # Page index buttons (tab).
    pc = Button(frtbpt, text="Constants",  command=change_to_frame('frc'))
    pc.grid(row = 0, column = 0)
    p1 = Button(frtbpt, text="1", command=change_to_frame('fr1'))
    p1.grid(row = 0, column = 1)
    p2 = Button(frtbpt, text="2", command=change_to_frame('fr2'))
    p2.grid(row = 0, column = 2)
    p3 = Button(frtbpt, text="3", command=change_to_frame('fr3'))
    p3.grid(row = 0, column = 3)

# Frame containing all widgets pertaining to constants
def framec():
    # Frame for all the small variable frames
    dFr['frc'] = Canvas(dFr['fr'],scrollregion = (0,0,1024,768))
    dBtn['bc'] = Button(dFr['frc'], text = "Constants Specified, Continue?", command=change_to_frame('fr1'))
    dBtn['bc'].grid(columnspan =3, rowspan = 2, sticky = N+S+W+E)
    dBtn['lpc'] = Label(dFr['frc'], text = "Constants fully specified")
    dBtn['lpcn'] = Label(dFr['frc'], text = " Constants have not been specified")
    dBtn['lpc'].grid(row = 2, columnspan = 3, pady = '2c')
    dBtn['btcold'] = Button(dFr['frc'], text = "Use original Values", command = btco)
    mcol = 3
    rw = 3
    i = 0
    while (i < (len(cnstnm))):
        col = 0
        while (i < len(cnstnm)) and (col <= (mcol-1)):
            lfrc = LabelFrame(dFr['frc'], text = cnstnm[i], labelanchor = 'nw')

            dCspb[cnstnm[i]] = Spinbox(lfrc,width = 6)
            dCspb[cnstnm[i]].insert(0,dCnst[cnstnm[i]])
            dCspb[cnstnm[i]].grid(row = 0, column = 0, padx = '1c',pady = '0.2c')
            dCspb[cnstnm[i]].event_add ( "<<allcnst>>", "<Button-1>", "<KP_Enter>" ,"<FocusOut>")
            dCspb[cnstnm[i]].bind("<<allcnst>>", cnstok)
            lc = Label(lfrc, text = cnstnm[i]) #Will add units later
            lc.grid(row = 0, column = 1, padx = '1c')

            lfrc.grid(row = rw, column = col, sticky = W+E,pady = '0.3c', padx = '0.1c')
            i = i + 1
            col = col + 1
        rw = rw + 1
    dFr['frc'].grid(row = 1, column = 0)

# Check if constants entered and update if changed
def cnstok(event):
    cnsts = [(dCspb[j].get()) for j in (cnstnm)]
    a = cnsts.count('')
    if a > 0:
        dBtn['lpcn'] = Label(dFr['frc'], text = str(a)+" Constant(s) NOT yet specified")
        dBtn['lpc'].grid_remove()
        dBtn['lpcn'].grid(row = 2, columnspan = 2, pady = '2c')
        dBtn['btcold'].grid(row = 2, column = 2, pady = '2c')
    else:
        dBtn['btcold'].grid_remove()
        dBtn['lpcn'].grid_remove()
        dBtn['lpc'].grid_remove()
        dBtn['lpc'].grid(row = 2, columnspan = 3, pady = '2c')
        for nmc in cnstnm:
            dCnst[nmc] = float(dCspb[nmc].get())
        print dCnst

# Insert original constants
def btco():
    cnsts = np.loadtxt('const.txt')
    [dCspb[nm].insert(0,cnsts[i]) for i, nm in enumerate(cnstnm)]
    dBtn['btcold'].grid_remove()
    dBtn['lpcn'].grid_remove()
    dBtn['lpc'].grid_remove()
    dBtn['lpc'].grid(row = 2, columnspan = 3, pady = '2c')

# Frame 1 - main form with all variables
def frame1():
    mcol = 8 # Maximum labelframes / column

    # Frame for each labelframes
    dFr['fr1'] = Canvas(dFr['fr'],scrollregion = (0,0,1024,768))

    # Place frame (label and edit) for each variable in names
    rownos = 0
    i = 0
    while (i < (len(names))):
        colnos = 0
        while (i < len(names)) and (colnos <= (mcol-1)):
            # create a new frame for each iteration in the loop
            lfr = LabelFrame(dFr['fr1'], text = names[i], labelanchor = 'nw')

            dSpb[names[i]] = Spinbox(lfr,width = 5)
            dSpb[names[i]].grid()
            dSpb[names[i]].event_add ( "<<allspb>>", "<Button-1>", "<KP_Enter>" ,"<FocusOut>")
            dSpb[names[i]].bind("<<allspb>>", sav)
            dScl[names[i]] = Scale(lfr,orient=HORIZONTAL,length = '4c')
            dScl[names[i]].grid()
            lfr.grid(row = rownos, column = colnos, sticky = W+E,pady = '0.3c', padx = '0.1c')


            i = i + 1
            colnos = colnos + 1
        rownos = rownos + 1

    scrollY = Scrollbar (dFr['fr1'],orient=VERTICAL, command = dFr['fr1'].yview )
    scrollY.grid (row = 0, rowspan = rownos, column=mcol+1, sticky=N+S+E )
    dFr['fr1']["yscrollcommand"] = scrollY.set

def frame2():
    dFr['fr2'] = Canvas(dFr['fr'],scrollregion = (0,0,1024,768))
    bp2 = Button(dFr['fr2'],text = "Page 2 Inactive")
    bp2.grid(row = 1, column = 1, pady = '2c')
    lp2 = Label(dFr['fr2'], text = "Reserved Cost")
    lp2.grid(row = 1, column = 2, pady = '2c')

def frame3():
    # Frame for all the small variable frames
    dFr['fr3'] = Canvas(dFr['fr'],scrollregion = (0,0,5000,900))
    bp3 = Button(dFr['fr3'],text = "Page 3 Inactive")
    bp3.grid(row = 1, column = 1, pady = '2c')
    lp3 = Label(dFr['fr3'], text = "Reserved Column Diagram")
    lp3.grid(row = 1, column = 2, pady = '2c')

def frame4():
    # Frame for all the small variable frames
    dFr['fr4'] = Canvas(dFr['fr'],scrollregion = (0,0,1500,900))
    bp4 = Button(dFr['fr4'],text = "Page 4 Inactive")
    bp4.grid(row = 1, column = 1, pady = '2c')
    lp4 = Label(dFr['fr4'], text = "Reserved for Cost Optimisation")
    lp4.grid(row = 1, column = 2, pady = '2c')

#Display relevant frame and remove the other (don't forget)
def change_to_frame(newframe):
    def changer():
        currentframe = dvar['crnt']
        dFr[currentframe].grid_remove()
        dFr[newframe].grid(row = 1, column = 0)
        dvar['crnt'] = newframe
    return changer

# Function which takes updates entry widgets when variables become specified from mofifier
def sav(event):
    for nm in dSpb.keys():
        if dSpb[nm].get() <> '':
            specv[nm] = float(dSpb[nm].get())
            #defV(specv, names, incidence, nm, float(dSpb[nm].get()))
    print specv

# Clear whichever field is in view
def clrspb():
    if dvar['crnt'] == 'fr1':
        for vspb in dSpb.keys():
            dSpb[vspb].delete(0,last=END)
            dSpb[vspb].insert(0,'')
        sp = {}
    if dvar['crnt'] == 'frc':
        for vcspb in dCspb.keys():
            dCspb[vcspb].delete(0,last=END)
            dCspb[vcspb].insert(0,'')
        dCnst = {}
    

# Call solve
def solv():
    for nm in dSpb.keys():
        if dSpb[nm].get() <> '':
            specv[nm] = float((dSpb[nm].get()))
            
    print specv
    sp = sc.solvr()
    print sp
    for nm in dSpb.keys():
        for var in sp:
            if nm == str(var):
                dSpb[nm].insert(1, sp.get(var))
                print sp.get(var)
        
    print "Solve Ran to Competion"


def odc():
    form = Tk()
    form.title("OMDDC")
    createWidgets(form,names)
    frame1()
    frame2()
    frame3()
    framec()
    form.mainloop()

odc()
