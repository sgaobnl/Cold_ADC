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
           [1, 1, "05us", "14mVfC", "900mV", "NoSDC"], 
           [2, 2, "10us", "14mVfC", "900mV", "NoSDC"],  
           [3, 3, "20us", "14mVfC", "900mV", "NoSDC"],  
           [4, 4, "30us", "14mVfC", "900mV", "NoSDC"],  
           
#
           ]
mode16bit = False
if (mode16bit):
    adc_bits = "ADC16bit"
else:
    adc_bits = "ADC12bit"
Cd="150pF"

nf_dir = "D:/ColdADC/D2_Cap_Study/"
nfr_dir = nf_dir + "results/"

tmpi = 0 
fig = plt.figure(figsize=(8,6))   
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
            rmss.append(np.std(np.array(chns[chnno][0:10000])&0xffff))
        else:
            rmss.append( np.std( (np.array( chns[chnno][0:10000] )&0xffff)//16))
    
    print (rmss)
    f_dir = "D:/ColdADC/D2_gainmeas_acq_Cap/"
    fr_dir = f_dir + "results/"
    g_testno_str = "Test%02d"%g_testno
    fs = file_list(runpath=fr_dir)
    for f in fs:
        if (f.find(g_testno_str)>=0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".csv")>0)and (f.find(adc_bits)>0)and (f.find(BL)>0):
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

    enc0 = [encs[0], encs[1], encs[8], encs[9]]
    enc22 = [encs[2], encs[10]]
    enc47 = [encs[3], encs[4], encs[11], encs[12]]
    enc82 = [encs[6], encs[14]]
    enc100 = [encs[5], encs[13]]
    enc150 = [encs[7], encs[15]]
    caps = [0, 22, 47, 82, 100, 150]
    print (list(encs))
#    encs_1chn = [encs[0], encs[2], encs[4], encs[6], encs[5], encs[7]]
    encs_avg = [np.mean(enc0), np.mean(enc22), np.mean(enc47), np.mean(enc82), np.mean(enc100), np.mean(enc150)]
    encs_std = [np.std(enc0), np.std(enc22), np.std(enc47), np.std(enc82), np.std(enc100), np.std(enc150)]
 #   plt.plot(caps,  encs_1chn,marker = 'o')
#    plt.plot(caps,  encs_avg,marker = '*')
    tmpi = tmpi + 1
    plt.errorbar(caps, encs_avg, encs_std, fmt = 'o', color = "C%d"%tmpi)
    results = sm.OLS(encs_avg ,sm.add_constant(caps)).fit()    
    slope = results.params[1]
    const = results.params[0]
    x = np.linspace(0, 150)
    y = x * slope + const
    plt.plot(x,y, label = "FE Tp = %s.%s: ENC = %.3f * Cap + %.2f"%(tp[0], tp[1:], slope, const), color = "C%d"%tmpi )
    plt.title("RT, FE sg = %s, , 12bit ADC"%(sg))
plt.xlim([-20, 180])
plt.xlabel("Input Capacitance / pF")
plt.ylim([0, 1500])
plt.ylabel("ENC / e-")
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig( nfr_dir + "caps" + sg + ".png")
plt.close()

#    plt.show()
#    enc_mean =int (np.mean(encs))
#    enc_std =int (np.std(encs))
#    test_ps[ty].append(enc_mean)
#    test_ps[ty].append(enc_std)
#    test_ps[ty].append(np.mean(rmss))
#    test_ps[ty].append(np.std(rmss))
#    test_ps[ty].append(np.mean(gains))
#    print (test_ps[ty])
#    
#    if (False):
#        chns = range(16)
#        fig = plt.figure(figsize=(4,9))
#        ax1 = plt.subplot2grid((6, 2), (0, 0), colspan=2, rowspan=2)
#        ax2 = plt.subplot2grid((6, 2), (2, 0), colspan=2, rowspan=2)
#        ax3 = plt.subplot2grid((6, 2), (4, 0), colspan=2, rowspan=2)
#        #    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
#        ax1.plot(chns, rmss, marker = '.')
#        ax2.plot(chns, gains, marker = '.')
#        ax3.plot(chns, encs, marker = '.', label = "Mean = %d"%enc_mean)
#        
#        ax3.legend()
#        
#        ax1.set_title("RMS Noise ")
#        ax2.set_title("Gain (e-/LSB)")
#        ax3.set_title("ENC (e-)")
#        
#        ax1.set_xlabel("Channel No")
#        ax2.set_xlabel("Channel No")
#        ax3.set_xlabel("Channel No")
#        
#        ax1.set_ylabel("RMS (LSB) ")
#        ax2.set_ylabel("Gain (e-/LSB)")
#        ax3.set_ylabel("ENC (e-)")
#        
#        xlim = (-2, 18) 
#        ax1.set_xlim(xlim)
#        ax2.set_xlim(xlim)
#        ax3.set_xlim(xlim)
#       
#        if (mode16bit):
#            ax1_ylim = (0, 200)
#            ax2_ylim = (0, 50)
#            ax3_ylim = (0, 1500)
#        else:
#            ax1_ylim = (0, 20)
#            ax2_ylim = (0, 1000)
#            ax3_ylim = (0, 1500)
#        ax1.set_ylim(ax1_ylim)
#        ax2.set_ylim(ax2_ylim)
#        ax3.set_ylim(ax3_ylim)
#        
#        ax1.grid(True)
#        ax2.grid(True)
#        ax3.grid(True)
#        
#        plt.tight_layout()
#        plt.savefig( nfr_dir + "NoiseTest%d"%test_ps[ty][0] +"_GainTest%d"%test_ps[ty][1] \
#                    + test_ps[ty][2] +test_ps[ty][3] + test_ps[ty][4] +test_ps[ty][5] + adc_bits +  ".png" )
#        plt.close()
#        
#fn = nfr_dir + "Test_result" + adc_bits +Cd +".bin"
#with open(fn, 'wb') as f:
#    pickle.dump(test_ps, f)

