#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:56:30 2019

@author: kovnerd
"""

import pandas as pd
import matlab.engine
import numpy
import scipy.io
import glob
import ast

def main():
    #read data from _ens file
    #read sim details from _details file
    temps = [];
    ensembleSize = -1;
    Ncor = -1;
    Ntherm = -1;
    name = input("name of run? (don't include ext) ");
    size = int(input("lattice size? "));
    files = glob.glob("../runs/" + name + "*" + "_" + str(size) +".txt");
    found = False;
    parsedData = pd.DataFrame();
    if(len(files) == 0):
        print("File not found!");
        return;
    else:
        for fname in files:
            if fname.find("_ens_") != -1:
                parsedData = pd.read_csv(fname, sep = " ");
                found = True;
                break;
            else:
                found = False;
        if(not found):
            print("Error, ensemble data not found!");
            return;
        for fname in files:
            #print(fname);
            if fname.find("_info_") != -1:
                with open(fname, "r") as infofile:
                    lines = infofile.readlines();
                    for i in range(len(lines)):
                        lines[i] = lines[i].split('=')[1];
                    size = ast.literal_eval(lines[0]);
                    temps = ast.literal_eval(lines[1]);
                    ensembleSize = ast.literal_eval(lines[2]);
                    Ncor = ast.literal_eval(lines[3]);
                    Ntherm = ast.literal_eval(lines[4]);
                    found = True;
                    break;
                break;
            else:
                found = False;
        if(not found):
                print("Error, run info not found!");
                return;
    print(parsedData);
    print("size = " + str(size));
    print("temps = " + str(temps));
    print("ensembleSize = " + str(ensembleSize));
    print("Ncor = " + str(Ncor));
    print("Ntherm = " + str(Ntherm));
    #DATA = matrix with dimensions [ensembleSize, 1] with data at T = 26
     
    eng = matlab.engine.start_matlab();
    row = parsedData[parsedData.Temperatures == 25.1327].values[0][1:];
    print(row);
    #data = numpy.asarray([row.iloc[1:].tolist()]);
    data = numpy.asarray(row);
    Stau = 1.5;#STAU = an initial guess as to tau/tauInt (not sure what this is??)
    Name = "\sigma^2";#NAME = name of observable to be used in plots ("sigma^2" or "\sigma^2"?)
    quantity = 1;
    Nrep = numpy.asarray([]); #NREP = a vector specifying how to break up the rows of DATA into replicas (set this to [ensembleSize]?)
    #scipy.io.savemat('Data.mat', {'Data':data});
    #scipy.io.savemat('Nrep.mat', {'Nrep':Nrep});
    scipy.io.savemat('UWerrInputs.mat', {'Data':data, 'Stau':Stau, 'Nrep':Nrep, 'Name':Name, 'Quantity':quantity});
    out = eng.UWerrPythonArgs(Stau,Name,quantity); #execute UWerr.m with above parameters
    #eng.load('Data.mat');
    #eng.transpose(eng.Data);
    #eng.load('Nrep.mat');
    #out = eng.UWerr(eng.Data,eng.double(Stau),eng.Nrep,eng.string(Name),eng.int64(quantity)); #execute UWerr.m with above parameters
    
    eng.quit();
main();
