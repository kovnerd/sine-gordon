#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:18:44 2019

@author: kovnerd
"""
import numpy
import sys
import os
import sine_gordon_info as sg
import sine_gordon_metropolis as met
import sine_gordon_hmc as hmc
import progressbar as pg
import pandas as pd
import time

#produces an ensemble at temperature T
def produce_ensemble_met(phi, T, eps, ensembleSize, Ncor, Ntherm):   
    sigma2s = [0 for n in range(0, ensembleSize)];
    avPhis = [0 for n in range(0, ensembleSize)];
    avPhis2 = [0 for n in range(0, ensembleSize)];
    avRejPerAcc = [0 for n in range(0, ensembleSize)];
    start = time.time();
    widgets = ['Thermalizing...', pg.Bar(marker = '=', left = '[', right = ']'), pg.Percentage()];
    bar = pg.ProgressBar(widgets = widgets, max_value = Ntherm).start();
    for therm in range(Ntherm):
         met.sweep(phi,1.0/T,eps);
         bar.update(therm);
    bar.finish()    
    print("approximate loops/second: " + str(Ntherm/(time.time()-start)));
    widgets = ['Accumulating data...', pg.Bar(marker = '=', left = '[', right = ']'), pg.Percentage()];
    bar = pg.ProgressBar(widgets = widgets, max_value = ensembleSize).start();
    for n in range(ensembleSize):
        accepts = 0;
        rejects = 0;
        for nc in range(Ncor):
            stats = met.sweep(phi, 1.0/T ,eps);
            accepts += stats[0];
            rejects += stats[1];
        #accumulate observables
        avPhis[n] = sg.avPhi(phi);
        avPhis2[n] = sg.avPhi2(phi);
        sigma2s[n] = avPhis2[n] - avPhis[n]*avPhis[n];
        bar.update(n);
        #avRejPerAcc[n] = 1.*rejects/accepts;
        #print("roughness = " + str(sigma2s[n]) + " reject/accept = " + str(avRejPerAcc[n]));
    bar.finish();
    return [avPhis, sigma2s, avRejPerAcc];

#produces an ensemble at temperature T
def produce_ensemble_hmc(phi, T, numSteps, length, ensembleSize, Ncor, Ntherm):   
    sigma2s = [0 for n in range(0, ensembleSize)];
    avPhis = [0 for n in range(0, ensembleSize)];
    avPhis2 = [0 for n in range(0, ensembleSize)];
    avRejPerAcc = [0 for n in range(0, ensembleSize)];
    for therm in range(0, Ntherm):
        hmc.sweep(phi, 1.0/T, numSteps, length);
    for n in range(0, ensembleSize):
        accepts = 0;
        rejects = 0;
        for nc in range (0, Ncor):
            stats = hmc.sweep(phi, 1.0/T, numSteps, length);
            accepts += stats[0];
            rejects += stats[1];
        #accumulate observables
        avPhis[n] = sg.avPhi(phi);
        avPhis2[n] = sg.avPhi2(phi);
        sigma2s[n] = avPhis2[n] - avPhis[n]*avPhis[n];
        avRejPerAcc[n] = 1.*rejects/accepts;
    return [avPhis, sigma2s,  avRejPerAcc];


#CURRENTLY AT FIXED SIZE!
#main part, actually do simulation:
#split up sim into different lattice sizes. Right now only focus on L=64
def generate_data(ensembleSize, Ncor, Ntherm, temps, size, data_file, data_file_ens):
    sigma2s = [0 for n in range(0, len(temps))];
    sigma2sErr = [0 for n in range(0, len(temps))];
    phi = [[0 for y in range(0,size)] for x in range(0, size)];
    data = pd.DataFrame({"Temperatures": temps});
    for i in range(ensembleSize):
        data.insert(len(data.columns), i, 0.0);
    
    for ntemp in range(0,len(temps)):
        bestEps = met.find_good_epsilon(temps[ntemp],1e-2);
        print("epsilon = " + str(bestEps) + " for temperature " + str(temps[ntemp]));
        observables = produce_ensemble_met(phi, temps[ntemp], bestEps, ensembleSize, Ncor, Ntherm);
        for i in range(len(observables[1])):
            data.iloc[ntemp, 1+i] = observables[1][i];
        sigma2s[ntemp] = numpy.average(observables[1]);
        sigma2sErr[ntemp] = numpy.std(observables[1]);
        sys.stdout.write("At T = " + str(temps[ntemp]) + ", av phi = " + str(numpy.average(observables[0])) + ", sigma^2 = "+ str(sigma2s[ntemp]) + "\n");
    data_file.writelines(str(sigma2s)+"\n");#write each ensemble as a column instead
    data_file.writelines(str(sigma2sErr));
    data.to_csv(data_file_ens, sep=' ', mode='w', index=False);
