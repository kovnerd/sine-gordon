#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:53:35 2019

@author: kovnerd
"""
import numpy
import sine_gordon_simulation as sim
import sys
import os
import progress

def main():
    #temps = [16.,20.,21.,22.,23.,24.,25.,26.,30.];
    temps = [25.1327];
    #sizes = [64,128,256,512,1024];
    ensembleSize = int(sys.argv[1]);
    Ncor = int(sys.argv[2]);
    sizes = [64];
    if 8*Ncor > 2048: 
        Ntherm = 8*Ncor; 
    else: 
        Ntherm = 2048;
    #print(Ntherm);
    name = input("Name the run? (don't include ext)");
    for size in sizes:
        if os.path.isfile("../runs/" + name + "_"+str(size)+".txt"):
            ans = input("clear first?[y,N] ");
            acceptable = False;
            while(not acceptable):
                if ans == "y" or ans == "Y":
                    data_file = open("../runs/" + name +  "_"+str(size)+".txt", "w");
                    data_file_ens = open("../runs/" +name + "_ens_" +str(size) + ".txt", "w");
                    acceptable = True;
                    print("cleared!");
                elif ans == "n" or ans == "N":
                    data_file = open("../runs/" + name + "_"+str(size)+".txt", "a");
                    data_file_ens = open("../runs/" + name + "_ens_"+ str(size) + ".txt", "a");
                    acceptable = True;
                    print("not cleared!");
                else:
                    print("invalid input, try again");
        else:
            data_file = open("../runs/"+name+"_"+str(size)+".txt", "w");
            data_file_ens = open("../runs/"+name + "_ens_"+str(size)  + ".txt", "w");
            print("made new file!");
        sim_details = open("../runs/" + name + "_info_" + str(size) + ".txt", "w");
        sim_details.writelines("L=" + str(size) + "\n");
        sim_details.writelines("temps=" + str(temps) + "\n");
        sim_details.writelines("ensembleSize=" + str(ensembleSize) + "\n");
        sim_details.writelines("Ncor=" + str(Ncor) + "\n");
        sim_details.writelines("Ntherm=" + str(Ntherm)+ "\n");
        data_file.writelines(str(temps) + "\n");
        print("Generating data for L = " + str(size));
        
        #collect the actual data
        sim.generate_data(ensembleSize, Ncor, Ntherm, temps, size, data_file, data_file_ens); 
        data_file.close();
        data_file_ens.close();
	#sim_details.close();

main();
