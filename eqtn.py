# -*- coding:utf-8 -*-
"""
Created on 24 Mar 2011

@author: Administrator
"""
from __future__ import division
import numpy as np
from math import *
import scipy.optimize as sc_op
from numpy.lib.scimath import log10

# Distillation equations
#function fnEq()
def fnEq(solvset,deq,varts,dcnst):

    #list of equations as a function of x
    # dictionary of equations represented using x['key'] as variables
    def eqt():
        return [lambda x , dcnst: x['Lo'] - dcnst['L/D']*dcnst['D'],
                lambda x , dcnst: x['V1'] - x['Lo'] - dcnst['D'],
                lambda x , dcnst: x['mL'] - dcnst['pL']*x['Lo'],
                lambda x , dcnst: x['mV'] - dcnst['pV']*x['V1'],
                lambda x , dcnst: x['Qc'] + dcnst['lambda']*(dcnst['D'] + x['Lo']),
                lambda x , dcnst: x['EntF'] - dcnst['Cpavg']*(x['Tf'] - dcnst['Tref']),
                lambda x , dcnst: x['EntB'] - x['mL']*dcnst['Cpavg']*(x['TbpB'] - dcnst['Tref']),
                lambda x , dcnst: x['Entd'] - x['mV']*(dcnst['lambda'] + dcnst['Cpavg']*(dcnst['Tref'] - x['TbpA'])),
                lambda x , dcnst: x['Qr'] + x['Qc'] + dcnst['F']*x['EntF'] - dcnst['B']*x['EntB'] - dcnst['D']*x['Entd'],
                lambda x , dcnst: x['lp'] - x['mult1']*x['do'],
                lambda x , dcnst: x['tw'] - x['mult2']*x['do'],
                lambda x , dcnst: x['Flv'] - (x['mL']/x['mV'])*sqrt(dcnst['pV']/dcnst['pL']),
                lambda x , dcnst: (x['uflood'])/0.3048 - x['Csbf']*((dcnst['sigma']/20)**0.2)*sqrt((dcnst['pL'] - dcnst['pV'])/dcnst['pV']),
                lambda x , dcnst: x['uop'] - dcnst['frac']*x['Csbf'],
                lambda x , dcnst: x['MWv'] - x['uop']*dcnst['pV'],
                lambda x , dcnst: x['Dc'] - sqrt((4*x['V1']*x['MWv'])/(pi*dcnst['n']*dcnst['pV']*dcnst['frac']*x['uflood']*3600)),
                lambda x , dcnst: x['x'] - ((x['thta'] - sin(x['thta']))/(2*pi)),
                lambda x , dcnst: x['lw'] - x['Dc']*sin(x['thta']/2),
                lambda x , dcnst: x['Ad'] - ((x['Dc']**2)/8)*(x['thta'] - sin(x['thta'])),
                lambda x , dcnst: x['lup'] - (x['Dc'] - 50*(10**(-3)))*((pi*x['thta'])/180),
                lambda x , dcnst: x['Aup'] - (50*10**(-3))*x['lup'],
                lambda x , dcnst: x['lcz'] - x['lw'] - 50*10**(-3),
                lambda x , dcnst: x['Acz'] - 2*(x['lcz']*(50*10**(-3))),
                lambda x , dcnst: x['Ac'] - (pi/4)*(x['Dc']**2),
                lambda x , dcnst: x['Aa'] - x['Ac'] + 2*x['Ad'],
                lambda x , dcnst: x['Ap'] - x['Aa'] + x['Aup'] + x['Acz'],
                lambda x , dcnst: x['Ah'] - 0.9*x['Ap']*((x['do']/x['lp'])**2),
                lambda x , dcnst: x['Ahole'] - (pi/4)*(x['do']**2),
                lambda x , dcnst: x['Nhole'] - (x['Ah']/x['Ahole']),
                lambda x , dcnst: x['Vo'] - ((x['V1']*x['MWv'])/(dcnst['pV']*x['Ah']*3600)),
                lambda x , dcnst: x['uh'] - (x['Vo']/x['Ah']),
                lambda x , dcnst: x['hd'] - 51*(dcnst['pV']/dcnst['pL'])*((x['uh']/x['CO'])**2),
                lambda x , dcnst: x['hw'] - 10*x['tw'],
                lambda x , dcnst: x['hap'] - x['hw'] + 10*10**(-3),
                lambda x , dcnst: x['how']/dcnst['pL'] - 750*((x['Lo']/(dcnst['pL']*x['lw']))**(2/3)),
                lambda x , dcnst: x['ht'] - x['hd'] - dcnst['hr'] - x['hw'] - x['how'],
                lambda x , dcnst: x['Aap'] - (x['hap']*x['lw']),
                lambda x , dcnst: x['hdc'] - 166*((x['mL']/(dcnst['pL']*x['Aap']))**2),
                lambda x , dcnst: x['hb'] - x['ht'] - x['hdc'] - x['hw'] - x['how'],
                lambda x , dcnst: log10(x['Csbf']) + 1 + 0.6*log10(x['Flv']) + 0.2*((log10(x['Flv']))**2),
                lambda x , dcnst: x['CO'] - 0.65 - 1.5*(x['Ah']/x['Ap'])]




    # function to pass to fsolve, return required equations with y[0],y[1]..
    def geteq(y):

        alleq = eqt()
        # list of functions
        eqlist = [alleq[(i)] for i in solvset]
        # list of equations in terms of dictionary x
        funceq = lambda x: [eq(x,dcnst) for eq in eqlist]
        # vartsc - var to solve copy, so dont intefere with vars
        vartsc = varts.copy()
        # deq - dictionary containing specified variables..
        # Add variables able to solve for as y[o], y[1] ... y[len(varts)] to deq
        for i,v in enumerate(vartsc):
            deq[v] = y[i]
        feq = funceq(deq)
        return feq

    # Initial values to fsolve = 1 for all **** Improvement later!

    ini = np.ones(len(solvset))
    soln = sc_op.fsolve(geteq,ini)
    return soln
