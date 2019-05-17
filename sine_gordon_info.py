#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:30:51 2019

@author: kovnerd
"""

import math
import numpy

#this is useful in metropolis
def action_local(phi,x,y,beta):#may need to add a term that forces the phi's to be less than 2pi
    L = len(phi);
    #PBC
    xNext = (x+1)%L;
    xPrev = (x-1)%L;
    yNext = (y+1)%L;
    yPrev = (y-1)%L;
    sumOverNeighbors = phi[xNext][y] + phi[x][yNext] + phi[xPrev][y] + phi[x][yPrev];
    return beta*(2*phi[x][y]*phi[x][y] - phi[x][y]*sumOverNeighbors - numpy.cos(phi[x][y]));

#this is useful in hmc?
def action_total(phi, beta):
    actionTot = 0.;
    L = len(phi);
    for x in range(0,L):
        xNext = (x+1)%L;
        for y in range(0,L):
            yNext = (y+1)%L;
            sumOverNeighbors = phi[xNext][y]+phi[x][yNext];
            sumOverNeighbors2 = phi[xNext][y]*phi[xNext][y] + phi[x][yNext]*phi[x][yNext]
            actionTot += phi[x][y]*phi[x][y] + 0.5*sumOverNeighbors2 - phi[x][y]*sumOverNeighbors - math.cos(phi[x][y]);
    return beta * actionTot;

#this is useful in hybrid monte carlo
def force_local(phi, x, y, beta):
    L = len(phi);
    xNext = (x+1)%L;
    xPrev = (x-1)%L;
    yNext = (y+1)%L;
    yPrev = (y-1)%L;
    sumOverNeighbors = phi[xNext][y] + phi[x][yNext] + phi[xPrev][y] + phi[x][yPrev];
    return beta*(4*phi[x][y] - sumOverNeighbors + math.sin(phi[x][y]));

#average of phi_i^n over the entire lattice
def avPhi(phi):
    L = len(phi);
    phiTot = 0.;
    for x in range(0,L):
        for y in range(0,L):
           phiTot += phi[x][y];
    return phiTot/(L*L);

def avPhi2(phi):
    L = len(phi);
    phiTot = 0.;
    for x in range(0,L):
        for y in range(0,L):
           phiTot += phi[x][y]*phi[x][y];
    return phiTot/(L*L);

def rough(phi):
    avphi = avPhi(phi);
    return avPhi2(phi) - avphi*avphi;