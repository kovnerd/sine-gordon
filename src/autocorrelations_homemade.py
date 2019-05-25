
import pandas as pd
import numpy
import math
import glob
import ast
from matplotlib import pyplot

#assuming invariance in time series index, not normalized
def autocorrelation(data, t):
    meanData = numpy.mean(data);
    dataSep = numpy.roll(data, -t);
    meanDataSep = numpy.mean(dataSep[:len(data)-t]);
    prod = numpy.multiply(data - meanData, dataSep - meanDataSep)[:len(data)-t];
    return numpy.mean(prod);

#figure out how to add axis titles and error bars
def plot_autocorrelation(data, figNum):
    print("plotting autocorrelation function...");
    autocorrs = [0 for x in range(0, len(data)//2)];
    norm = autocorrelation(data,0);
    for t in range(len(data)//2):
        autocorrs[t] = autocorrelation(data, t)/norm;
    ts = [x for x in range(0, 4000)];
    fig = pyplot.figure(figNum);
    pyplot.title("\Gamma(t) for various summation windows");
    pyplot.plot(ts, autocorrs[:len(ts)]);
    
#computed integrated autocorrelation time with finite sum
#bias corrects for cutting off infinite sum
def integrated_autocorrelation_time(data, upperBound, bias):
    tauint = 0.5;
    norm = autocorrelation(data, 0) + bias;
    for t in range(1, upperBound):
        tauint += (autocorrelation(data,t) + bias)/norm;
    return tauint;

#plots autocorrelation time v.s. summation window/upperBound.
#This is computed inefficiently...
#figure out how to add axis titles and error bars
def plot_tau_int(data, upperBound, figNum):
    print("plotting tau_int...");
    ts = [x for x in range(0, 2*upperBound)]; 
    tauints = [0 for x in range(len(data)//2)];
    tauints[0] = 0.5;
    copt = autocorrelation(data, 0);
    norm = copt;
    #correct the finite series bias in tauInt
    for t in range(1, len(ts)):
        copt += 2*autocorrelation(data, t);
        bias = copt/len(data);
        tauints[t] = tauints[t-1]+(autocorrelation(data, t)+bias)/(norm+bias); 
    pyplot.figure(figNum);
    pyplot.title("\\tau_{int} for various summation windows");
    pyplot.plot(ts, tauints[:len(ts)]);

def autocor_error_analysis(data, S):
    tauW = 0.5;
    gammaNormedInt = 1;
    tauInts = [0.5];
    tauIntCurrent = 0.5;
    gW = 0.5;
    norm = autocorrelation(data,0);
    #try to do automatic windowing
    for w in range(1,len(data)//2):
        gammaNormedInt += autocorrelation(data, w)/norm;
        if gammaNormedInt <= 0:
            tauW = 1e-6;
        else:
            tauW = S/math.log((gammaNormedInt+1)/(gammaNormedInt));
        gW = math.exp(-w/tauW) - tauW/(math.sqrt(w*len(data)));
        if(gW < 0):
            wOpt = w;
            break;
    copt = norm;
    for t in range(1, wOpt):
       copt += 2*autocorrelation(data, t);
    bias = copt/len(data);
    err = math.sqrt((1+(2*wOpt+1)/len(data))*bias);
    #errErr = ...;
    tauInt = integrated_autocorrelation_time(data, w, bias);
    tauErr = 2*tauInt*math.sqrt((wOpt + 0.5 - tauInt)/len(data));
    print("window W = " + str(wOpt));
    print("error in observable = " + str(err));
    #print("error in the error of the observable" + str(errErr)); 
    print("resulting tauint = " + str(tauInt));
    print("error in tauint = " + str(tauErr));
    
    return [wOpt, err, tauInt, tauErr];

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

    #set up time series from parsed data
    for t in temps:
        row = parsedData[parsedData.Temperatures == t].values[0][1:];
        print(row); 
        errorInfo = autocor_error_analysis(row, 1.5);
        plot_autocorrelation(row, 1);
        plot_tau_int(row, errorInfo[0], 2);
        pyplot.show();
main();
