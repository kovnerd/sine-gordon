function [value,dvalue,ddvalue,tauint,dtauint,Qval] = UWerrPythonArgs(Stau,Name,Quantity,varargin)

load('UWerrInputs.mat');
%load('Data.mat');
Data = transpose(Data);
%load('Nrep.mat');
Nrep = transpose(Nrep);

%[value,dvalue,ddvalue,tauint,dtauint,Qval] = UWerr(Data, double(Stau), Nrep, string(Name), int64(Quantity))
[value,dvalue,ddvalue,tauint,dtauint,Qval] = UWerr(Data, Stau, Nrep, Name, Quantity)
