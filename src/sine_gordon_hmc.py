#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 22:47:42 2019

@author: kovnerd
"""
import numpy
import math
import random

import sine_gordon_info as sg
        
def generate_momenta(L, width):
    p = numpy.zeros((L,L));
    for x in range(0, p.shape[0]):
        for y in range(0, p.shape[1]):
            p[x][y] = numpy.random.normal(0,width); 
    return p;

def reset_momenta(p, width):
    for x in range(0, p.shape[0]):
        for y in range(0, p.shape[1]):
            p[x][y] = numpy.random.normal(0,width); 

def hamiltonian(phi, p, beta):
    kinetic = 0.;
    for i in range(0,p.shape[0]):
        for j in range(0, p.shape[1]):
            kinetic += 0.5*p[i][j]*p[i][j];
    return kinetic + sg.action_total(phi,beta);

def iterate_p(phi, p, beta, stepSize):
    for x in range(0, p.shape[0]):
        for y in range(0, p.shape[1]):
            p[x][y] -= stepSize*sg.force_local(phi,x,y,beta);

def iterate_phi(phi, p, beta, stepSize):
     for x in range(0, p.shape[0]):
        for y in range(0, p.shape[1]):
            phi[x][y] += stepSize*p[x][y];

#one step of a leap frog integrator, defined in terms of move operations
def leap_frog_step(phi, p, beta, stepSize):
    iterate_phi(phi,p,beta,0.5*stepSize);
    iterate_p(phi,p,beta,stepSize);
    iterate_phi(phi,p,beta,0.5*stepSize);
    
        
#does 1 hybrid monte carlo update using the leapfrog integration method      
def sweep(phi, p, beta, numSteps, length):
    accepts = 0;
    rejects = 0;
    stepSize = 1.*length/numSteps;
    #figure out what the optimum width is for the momentum!!!!!
    #initialize momentum
    phiBefore = phi;
    pBefore = p;
    oldH = hamiltonian(phi,p,beta);
    #evolve trajectory with a leap frog integrator
    for i in range(0, numSteps):
        leap_frog_step(phi, p, beta, stepSize);
    #accept trajectory with metropolis probability
    deltaH = hamiltonian(phi,p,beta) - oldH;
    if(deltaH > 0 and random.uniform(0,1) > math.exp(-deltaH)):
        phi = phiBefore;
        p = pBefore;
        rejects+=1;
    else:
        accepts+=1;  
    sg.shift(phi);
    return [accepts,rejects];

def reversability_check(tolerance):
    #copy/paste code for 1 trajectory. 
    L=16;
    phi = numpy.ones((L,L));
    length = 64.;
    numSteps = 128;
    stepSize = length/numSteps;
    p = generate_momenta(L, 1); 
    phiInit = phi;
    pInit = p;
    pDiff = numpy.ones((L,L));
    phiDiff = numpy.ones((L,L));
    passed = False;
    #evolve trajectory
    for i in range(0, numSteps):
       leap_frog_step(phi, p, 1., stepSize);
    
    #flip momenta, evolve trajectory back;
    p *= -1;
    for i in range(0, numSteps):
        leap_frog_step(phi, p, 1., stepSize);
        
    #flip check if the resulting momentum are the same as the initial ones
    for x in range(0, pInit.shape[0]):
        for y in range(0, pInit.shape[1]):
            pDiff[x][y] = abs(pInit[x][y]-p[x][y]);
            phiDiff[x][y] = abs(phiInit[x][y] - phi[x][y]);
    for x in range(0, phiDiff.shape[0]):
        for y in range(0, phiDiff.shape[1]):
            if(pDiff[x][y] < tolerance and phiDiff[x][y] < tolerance):
                passed = True;
            else:
                return False;
    return passed;
    
    
#optimizes the stepSize such that an hmc sweep is accepted with 40 prop
def optimize_acceptance(L, length, numSteps, rate, tolerance):
    Ltest = 16;
    Ntest = int(L*L)/int(Ltest*Ltest)
    phiTest = numpy.pi*numpy.ones((Ltest,Ltest))
    pTest = generate_momenta(Ltest, 1);
    accepts = 0;
    rejects = 0;
    stepSizes = length/numSteps * numpy.ones((Ltest, Ltest));
    B = tolerance + 1.;
    for t in range(0, 4096):
        sweep(phiTest, pTest, 1., numSteps, 1);#thermalize a little before finding good epsilons 
    for n in range(0,100):
        while(abs(B) > tolerance):#
            accepts = 0;
            rejects = 0;
            for i in range(0, Ntest):
                reset_momenta(pTest, 1.);
                temp = sweep(phiTest,1., );#temperature = 1 for convenience
                accepts += temp[0];
                rejects += temp[1];
                B = rate/(1.-rate) - (1.*rejects)/accepts;#bias < 0 if more rejects have been made, > 0 if more accepts have been made
                stepSizes[n] += (B*B*B + B);
    return numpy.average(stepSizes);   