# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 00:00:54 2019

@author: protoDUNE
"""

import numpy as np
import os
from sys import exit
import os.path
import math
import time
import statsmodels.api as sm

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.mlab as mlab

import pickle

def file_list(runpath):
    if (os.path.exists(runpath)):
        for root, dirs, files in os.walk(runpath):
            break
    return files

test_ps = [
           [1, 1, "05us", "14mVfC"], 
           [2, 2, "10us", "14mVfC"],  
           [3, 3, "20us", "14mVfC"],  
           [4, 4, "30us", "14mVfC"],  

           [11, 11, "05us", "47mVfC"], 
           [12, 12, "10us", "47mVfC"],  
           [13, 13, "20us", "47mVfC"],  
           [14, 14, "30us", "47mVfC"],  

           [21, 21, "05us", "78mVfC"], 
           [22, 22, "10us", "78mVfC"],  
           [23, 23, "20us", "78mVfC"],  
           [24, 24, "30us", "78mVfC"],  
           
           [31, 31, "05us", "25mVfC"],  
           [32, 32, "10us", "25mVfC"],  
           [33, 33, "20us", "25mVfC"],  
           [34, 34, "30us", "25mVfC"],  
 
  
           ]
mode16bit = True
for ty in range(len(test_ps)):
    noise_testno = test_ps[ty][0] 
    g_testno = test_ps[ty][1] 
    tp =  test_ps[ty][2]
    sg =  test_ps[ty][3]
    
    if (mode16bit):
        adc_bits = "ADC16bit"
    else:
        adc_bits = "ADC12bit"

    f_dir = "D:/ColdADC/D2_noise_acq/"
    fr_dir = f_dir + "results/"
    if (os.path.exists(fr_dir)):
        pass
    else:
        try:
            os.makedirs(fr_dir)
        except OSError:
            print ("Error to create folder ")
            exit()
    
    noise_testno_str = "Test%02d"%noise_testno
    fs = file_list(runpath=f_dir)
    for f in fs:
        if (f.find(noise_testno_str)>0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".bin")>0):
            fn = f_dir + f
            break
    with open (fn, 'rb') as fp:
        chns = pickle.load(fp)
    rmss = []
    for chnno in range(16):
        if (mode16bit):
            rmss.append(np.std(np.array(chns[chnno][0:10000])&0xffff))
        else:
            rmss.append( np.std( (np.array( chns[chnno][0:10000] )&0xffff)//16))
    
    
    f_dir = "D:/ColdADC/D2_gainmeas_acq/"
    fr_dir = f_dir + "results/"
    g_testno_str = "Test%02d"%g_testno
    fs = file_list(runpath=fr_dir)
    for f in fs:
        if (f.find(g_testno_str)>=0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".csv")>0)and (f.find(adc_bits)>0):
            gfn = fr_dir + f
            break
    
    ccs = []
    with open(gfn, 'r') as fp:
        for cl in fp:
            tmp = cl.split(",")
            x = []
            for i in tmp:
                x.append(i.replace(" ", ""))
            x = x[:-1]
            ccs.append(x)
            
    gains = []        
    for i in range(len(ccs[0])):
        gains.append(float(ccs[0][i]) )
    
    
    encs = np.array(rmss)*np.array(gains)
    enc_mean =int (np.mean(encs))
    enc_std =int (np.std(encs))
    test_ps[ty].append(enc_mean)
    test_ps[ty].append(enc_std)
    test_ps[ty].append(np.mean(rmss))
    test_ps[ty].append(np.std(rmss))
    test_ps[ty].append(np.mean(gains))
    print (test_ps[ty])
    
    chns = range(16)
    fig = plt.figure(figsize=(8,6))
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=4)
    #    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
    ax1.plot(chns, rmss, marker = '.')
    ax2.plot(chns, gains, marker = '.')
    ax3.plot(chns, encs, marker = '.', label = "Mean = %d"%enc_mean)
    
    ax3.legend()
    
    ax1.set_title("RMS Noise ")
    ax2.set_title("Gain (e-/LSB)")
    ax3.set_title("ENC (e-)")
    
    ax1.set_xlabel("Channel No")
    ax2.set_xlabel("Channel No")
    ax3.set_xlabel("Channel No")
    
    ax1.set_ylabel("RMS (LSB) ")
    ax2.set_ylabel("Gain (e-/LSB)")
    ax3.set_ylabel("ENC (e-)")
    
    ax1.set_xlim((-2,18))
    ax2.set_xlim((-2,18))
    ax3.set_xlim((-2,18))
    
    ax1.set_ylim((0,10))
    ax2.set_ylim((0,1000))
    ax3.set_ylim((0,1000))
    
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    
    plt.tight_layout()
    plt.savefig( fr_dir + "NoiseTest%d"%test_ps[ty][0]  +"_GainTest%d"%test_ps[ty][1] + test_ps[ty][2] +test_ps[ty][3] + adc_bits +  ".png" )
    plt.close()


