#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:56:30 2019

@author: kovnerd
"""

import pandas as pd
#import matlab.engine
import glob
import ast

def main():
    #read data from _ens file
    #read sim details from _details file
    temps = [];
    ensembleSize = 0;
    Ncor = 0;
    Ntherm = 0;
    name = raw_input("name of run? (don't include ext) ");
    size = int(raw_input("lattice size? "));
    files = glob.glob("runs/" + name + "*" + "_" + str(size) +".txt");
    found = False;
    data = pd.DataFrame();
    if(len(files) == 0):
        print("File not found!");
        return;
    else:
        for fname in files:
            if fname.find("_ens_") != -1:
                data = pd.read_csv(fname, sep = " ");
                found = True;
                break;
            else:
                found = False;
        if(not found):
            print("Error, ensemble data not found!");
                
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
    print(data);
    print("size = " + str(size));
    print("temps = " + str(temps));
    print("ensembleSize = " + str(ensembleSize));
    print("Ncor = " + str(Ncor));
    print("Ntherm = " + str(Ntherm));
    #DATA = matrix with dimensions [ensembleSize, 1] with data at T = 26
    #data.
    
    Stau = 1.5;#STAU = an initial guess as to tau/tauInt (not sure what this is??)
    Nrep = [ensembleSize]; #NREP = a vector sspecifying how to break up the rows of DATA into replicas (set this to [ensembleSize]?)
    Name = "\sigma^2";#NAME = name of observable to be used in plots ("sigma^2" or "\sigma^2"?)
    quantity = 1;
    
    eng = matlab.engine.start_matlab();
    out = eng.UWerr(convertedData,Stau,Nrep,Name,quantity, nargout=6);
    eng.quit();
    
    #execute UWerr.m with above parameters
main();