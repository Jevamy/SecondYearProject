# -*- coding: utf-8 -*-
"""
Created on Sun Nov 03 20:32:01 2013

INSTRUCTIONS
~~~~~~~~~~~~

This is a template file for you to use for your Computing 2 Coursework.

Save this file as py12spqr.py when py12spqr should be replaced with your ISS username

Do not rename or remove the function ProcessData, the marking will assume that this function exists
and will take in the name of a data file to open and process. It will assume that the function will return
all the answers your code finds. The results are returned as a dictionary.

Your code should also produce the same plot as you produce in your report.

@author: phygbu
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import curve_fit
from scipy import integrate


"""This code will return a Lorentzian curve for a set of differential noisy data.
It also integrates multiple columns of data"""
 
try:
    with open("assessment_data_py13jej.dat", 'r') as d:                  #multi diff data with noise
        #r = d.read().splitlines()                                   #reads file lines 
        count = 0  
        for line in d:
            count += 1                                              #keeps a record of how many lines of metadata skipped
            if '&END' in line:                                       #skips to end of metadata
                break 
except:
    IOError
 

f = [] #empty list to append data to
def frequency(f):
    try:
        idata = np.genfromtxt("assessment_data_py13jej.dat",     #data with metadata skipped
                          skip_header=count , delimiter = '\t',  #goes to frequency line
                          dtype =None) 
      #empty list to put frequencies in
        for line in idata[0]:                                    #appends 1st row values(frequencies) to frequency list
            f.append(line) 
        f = f[1:]                                                #slices of 'Magnetic Field' element
    except:
        IOError

frequency(f)
ind = f.index(20.0)                                             #locates position of 20GHz column in data
data = np.genfromtxt("assessment_data_py13jej.dat",             #all useful data
                  skip_header=count+1 , delimiter = '\t')            
x = data[:,0]                                                   #sets x as H field value(first column)
twenty = np.genfromtxt("assessment_data_py13jej.dat",           #20ghz column
                  skip_header=count+1 , delimiter = '\t'
                  , usecols = ind)
yint20 = integrate.cumtrapz(twenty,x, initial = 0)              #integrate 20 GHz column
yintall = []                                                    #empty list to integrate data into
       
def intY():
    """integrate all columns of absorption data"""
    try:
        for a in range(1,len(f),1):                            #range along columns
            b = integrate.cumtrapz(data[:,a], x, initial = 0)  #integrate all frequency columns
            yintall.append(b)                                  #create list of integrated columns
    except:                                                    #function not actually used due to errors in Kittelfit section
        IOError


def Lorentzian(x, h0,dh,c):                                    #Lorentzian func to fit curve to data c = some constant
    """Function to fit Lorentzian"""    
    try:    
        Lorentz = c *(1/(2*np.pi)) * dh * (((x-h0)**2 + (dh/2)**2)**-1) #equation from Tasksheet
        return Lorentz * 7.9495E5                              #converting to Tesla
    except:
        IOError

def H0data(x,yint20): 
    """Return H0 Peak Position from the Curve""" 
    try:
        p,pcov = curve_fit(Lorentzian,x,yint20, p0 = [100000,30000,1]) #Fitting the Lorentzian with guesses for H0,dh,c
        err = scipy.sqrt(scipy.diag(pcov))                             #finding errors in fit
        H0 = p[0]                                                      #sets H0 as x value of peak
        return H0
        return err[0]                                            #Peak positions, constant, Peak pos error from diag.pcov, 
    except:
        IOError                                          
def dhdata(x,yint20):
    """Return dh Peak Width from the curve"""
    try:
        p,pcov = curve_fit(Lorentzian,x,yint20, p0 = [100000,30000,1]) 
        err = scipy.sqrt(scipy.diag(pcov))
        dh = p[1]                                                     #Sets dh as peak width
        return dh 
        return err[1]                                                  #dh Error from diag.pcov
    except:
        IOError
def plot_twenty():
    """Plots integrated 20GHz data"""
    dh = dhdata(x,yint20)                                   #dh must be defined to use as text positioner     
    H0 = H0data(x,yint20)                                        # calling H0 to use for annotations              
    Peak = np.max(yint20)                                          # Peak y value for 20GHz
    plt.figure()
    plt.plot(x,yint20)    
    plt.ylabel ("Absorption")
    plt.xlabel ("Integrated Magnetic Field (A/m)")
    plt.title ("py13jej Integrated Data")
    plt.annotate('20Ghz', xy=(H0, Peak), xytext=((0.5*H0), 0.8*Peak),   #setting arrow so its a suitable 
            arrowprops=dict(arrowstyle='->')                                #distance from peak to ensure legibility
            )
    plt.text(1.2*H0, 0.7*Peak, '$\Delta$H = %s\n H0 = %s\n' % (dh,H0))  #placing text at appropriate location
    plt.show()        

def ProcessData(filename):
    """Documentation string here."""
    plot_twenty()#Your code goes here
    results={"20GHz_peak":H0data(x,yint20), #this would be the peak position at 20GHz
             "20GHz_width":dhdata(x,yint20), #Delta H for 20 GHz
             "gamma": None, #your gamma value
             "g": None, #Your Lande g factor

    #If your code doesn't find all of these values, just leave them set to None
    #Otherwise return the number. Your report should also give the errors in these numbers.

    return results

if __name__=="__main__":
    # Put your test code in side this if statement to stop it being run when you import your code
    #Please avoid using raw_input as the testing is going to be done by a computer programme, so
    #can't input things from a keyboard....
    filename="My Data File.txt"
    test_results=ProcessData(filename)
    print test_results