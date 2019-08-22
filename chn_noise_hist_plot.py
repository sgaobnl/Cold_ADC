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
#            [91, 2, "10us", "14mVfC", "900mV", "NoSDC"], 
#            [92, 2, "10us", "14mVfC", "900mV", "SDC"],             
#           [1, 1, "05us", "14mVfC", "200mV", "NoSDC"], 
#           [2, 2, "10us", "14mVfC", "200mV", "NoSDC"],  
#           [3, 3, "20us", "14mVfC", "200mV", "NoSDC"],  
#           [4, 4, "30us", "14mVfC", "200mV", "NoSDC"],  
#           [5, 5, "05us", "14mVfC", "200mV", "SDC"], 
#           [6, 6, "10us", "14mVfC", "200mV", "SDC"],  
#           [7, 7, "20us", "14mVfC", "200mV", "SDC"],  
#           [8, 8, "30us", "14mVfC", "200mV", "SDC"],  
#           
#           [1, 1, "05us", "14mVfC", "900mV", "NoSDC"], 
#           [2, 2, "10us", "14mVfC", "900mV", "NoSDC"],  
#           [3, 3, "20us", "14mVfC", "900mV", "NoSDC"],  
#           [4, 4, "30us", "14mVfC", "900mV", "NoSDC"],  
#
#           [11, 11, "05us", "47mVfC", "900mV", "NoSDC"], 
#           [12, 12, "10us", "47mVfC", "900mV", "NoSDC"],  
#           [13, 13, "20us", "47mVfC", "900mV", "NoSDC"],  
#           [14, 14, "30us", "47mVfC", "900mV", "NoSDC"],  
#
#           [21, 21, "05us", "78mVfC", "900mV", "NoSDC"], 
#           [22, 22, "10us", "78mVfC", "900mV", "NoSDC"],  
#           [23, 23, "20us", "78mVfC", "900mV", "NoSDC"],  
#           [24, 24, "30us", "78mVfC", "900mV", "NoSDC"],  
#           
#           [31, 31, "05us", "25mVfC", "900mV", "NoSDC"],  
#           [32, 32, "10us", "25mVfC", "900mV", "NoSDC"],  
#           [33, 33, "20us", "25mVfC", "900mV", "NoSDC"],  
#           [34, 34, "30us", "25mVfC", "900mV", "NoSDC"],  
#
#           [5, 5, "05us", "14mVfC", "900mV", "SDC"], 
#           [6, 6, "10us", "14mVfC", "900mV", "SDC"],  
#           [7, 7, "20us", "14mVfC", "900mV", "SDC"],  
#           [8, 8, "30us", "14mVfC", "900mV", "SDC"],  
#
#           [15, 15, "05us", "47mVfC", "900mV", "SDC"], 
#           [16, 16, "10us", "47mVfC", "900mV", "SDC"],  
#           [17, 17, "20us", "47mVfC", "900mV", "SDC"],  
#           [18, 18, "30us", "47mVfC", "900mV", "SDC"],  
#
#           [25, 25, "05us", "78mVfC", "900mV", "SDC"], 
#           [26, 26, "10us", "78mVfC", "900mV", "SDC"],  
#           [27, 27, "20us", "78mVfC", "900mV", "SDC"],  
#           [28, 28, "30us", "78mVfC", "900mV", "SDC"],  
#           
#           [35, 35, "05us", "25mVfC", "900mV", "SDC"],  
#           [36, 36, "10us", "25mVfC", "900mV", "SDC"],  
#           [37, 37, "20us", "25mVfC", "900mV", "SDC"],  
#           [38, 38, "30us", "25mVfC", "900mV", "SDC"],  

           ]
mode16bit = True
if (mode16bit):
    adc_bits = "ADC16bit"
else:
    adc_bits = "ADC12bit"

nf_dir = "D:/ColdADC/D2_noise_acq/"
nfr_dir = nf_dir + "results/"
    
for ty in range(len(test_ps)):
    noise_testno = test_ps[ty][0] 
    g_testno = test_ps[ty][1] 
    tp =  test_ps[ty][2]
    sg =  test_ps[ty][3]
    BL = test_ps[ty][4]
    

    f_dir = nf_dir
    fr_dir = nfr_dir
    
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
        if (f.find(noise_testno_str)>0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".bin")>0) and (f.find(BL)>0):
            fn = f_dir + f
            break
    with open (fn, 'rb') as fp:
        chns = pickle.load(fp)
    rmss = []
    for chnno in range(16):
        if (mode16bit):
            data_slice = np.array(chns[chnno][0:10000])&0xffff
        else:
            data_slice = (np.array(chns[chnno][0:10000])&0xffff)//16
    
    if (True):
        chns = range(16)
        fig = plt.figure(figsize=(4,4))

        for chnno in chns:
            ax = plt.subplot2grid((4, 4), (chnno//4, chnno%4), colspan=1, rowspan=1)

            N = len(data_slice)
            sigma3 = int(rms+1)*3
            ax.hist(data_slice, normed=1, bins=sigma3*2, range=(ped-sigma3, ped+sigma3),  histtype='bar', label="CH%d"%chnno, color='b', rwidth=0.9 )
            gaussian_x = np.linspace(ped - 3*rms, ped + 3*rms, 100)
            gaussian_y = mlab.normpdf(gaussian_x, ped, rms)
            ax.plot(gaussian_x, gaussian_y, color='r')

            ax.grid(True)
            ax.set_title(title + "(%d samples)"%N )
            ax.set_xlabel("ADC output / LSB")
            ax.set_ylabel("Normalized counts")
            ax.legend(loc='best')

        plt.tight_layout()
        plt.savefig( nfr_dir + "HIST_NoiseTest%d"%test_ps[ty][0] + test_ps[ty][2] +test_ps[ty][3] + test_ps[ty][4] +test_ps[ty][5] + adc_bits +  ".png" )
        plt.close()
