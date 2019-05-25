#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:23:07 2019

@author: kovnerd
"""
import glob
import ast
import matplotlib.pyplot as plt

def main():
    #read data from _ens file
    #read sim details from _details file
    temps = [16.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 30.0];#don't read this from file, know this beforehand...
    sizes = [];
    sigma2s = [];#sigma2s[sizeIndex][tempIndex]
    markers = ['^', 'D', 's', '+', 'x', '.', '*', 'H', '1'];#different type of markers for plot
    name = input("name of run? (don't include ext) ");
    files = glob.glob("../runs/" + name + "_" +  "*" +".txt");
    print(files);
    if(len(files) == 0):
        print("File not found!");
        return;
    else:
        #collect sizes and sigma2s from appropriate files
        for fname in files:
            print(fname);
            parse = fname.split('.')[0].split('_')[-1];
            if parse.isdigit() == True and fname.find('_ens_') == -1 and fname.find('_info_') == -1:
                sizes.append(int(parse));
                lines = open(fname, "r").readlines();
                print(lines);
                #print(lines[1].split('=')[0].split('\n'))[0];
                lines[1] = lines[1].split('=')[0].split('\n')[0];
                sigma2s.append(ast.literal_eval(lines[1]));
    #switch indices fo sigma2s, because it was easier to load form .txt the other way
    tmp = [[0 for l in range(len(sizes))] for t in range(len(temps))];
    for l in range(len(sizes)):
        for t in range(len(temps)):
          tmp[t][l] = sigma2s[l][t]; 
    sigma2s = tmp;
    #print(sigma2s);
    #load plot
    for t in range(len(temps)):
        plt.plot(sizes, sigma2s[t], markers[t], label = "T="+str(temps[t]));
    plt.ylim(10.0, 37.5);
    plt.legend(loc = 'upper right');
    plt.show();
                    
                        
            
    
main();
