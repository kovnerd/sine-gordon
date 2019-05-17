# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:18:44 2019

@author: kovnerd
"""
import numpy
import math
import sine_gordon_info as sg

def shiftNearest2Pi(phi):
    phiAv = sg.avPhi(phi);
    L = len(phi);
    for x in range(0, L):
        for y in range(0, L):
            phi[x][y] -= 2.0*numpy.pi*round(phiAv/(2.0*numpy.pi));

def sweep(phi,beta,eps):    
    L = len(phi);
    accepts = 0;
    rejects = 0;
    for x in range(0, L):
        for y in range(0, L):
            phiBefore = phi[x][y];
            actionBefore = sg.action_local(phi,x,y,beta);
            #actionBefore = sg.action_total(phi,beta);
            phi[x][y] = numpy.random.normal(phi[x][y], eps);
            deltaAction = sg.action_local(phi,x,y,beta)-actionBefore;
            #deltaAction = sg.action_total(phi,beta)-actionBefore;   
            if(deltaAction > 0 and math.exp(-deltaAction) < numpy.random.uniform()):
                phi[x][y] = phiBefore;
                rejects+=1;
            else:
                accepts+=1; 
    shiftNearest2Pi(phi);
    return [accepts,rejects];

def find_good_epsilon(T, tolerance):
    Ltest = 8;
    phi = [[0 for x in range(0, Ltest)] for y in range(0, Ltest)];
    nSteps = 100;
    eps = 4;
    bias = 2*tolerance;
    while(abs(bias) > tolerance):
        avRejPerAcc = 0;
        for therm in range(0, 4*nSteps):
            sweep(phi, 1./T, eps);
        accepts = 0;
        rejects = 0;
        for nc in range (0, nSteps):
            stats = sweep(phi,1./T, eps);
            accepts += stats[0];
            rejects += stats[1];
        avRejPerAcc = (1.*rejects)/accepts;
        #print("using gaussian with width " + str(eps) + " to make metropolis moves:")
        #print("accept/reject over " + str(nSteps) + " sweeps: " + str(avRejPerAcc) + "\n");
        bias = (1. - (avRejPerAcc));
        eps += bias + bias*bias*bias;
    return eps;