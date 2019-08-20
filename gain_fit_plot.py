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
from asic_dac_fit import asic_dac_fit

def file_list(runpath):
    if (os.path.exists(runpath)):
        for root, dirs, files in os.walk(runpath):
            break
    return files

def Asic_Cali(data_fs, mode16bit = True):
    asic_info = []
    for asic_dac in range(3,16,1):
        for f in data_fs:
            if f.find("asicdac%02d"%asic_dac) > 0:
                fn = f_dir + f
                break
        with open (fn, 'rb') as fp:
            chns = pickle.load(fp)
    
        poft = 0
        for j in range(period):
            if ((chns[0][j]&0x10000) & 0x10000) > 0:
                poft = j
                if poft <50:
                    poft = 200+poft-50
                else:
                    poft = poft-50
                break
    
        chns_info = []
        for chnno in range(len(chns)):
            for i in range(0,avg_n):
                if i == 0:
                    avg_chns = (np.array(chns[chnno][poft+200*i:poft+200+200*i])&0xffff)
                else:
                    avg_chns = avg_chns + (np.array(chns[chnno][poft+200*i:poft+200+200*i])&0xffff)
            avg_chns = avg_chns//avg_n
            chn_pkp = np.max(avg_chns)  
            chn_pkn = np.min(avg_chns)
            chn_ped = (avg_chns[0])  
            chn_ploc = np.where( avg_chns == chn_pkp )[0][0]
            if (mode16bit):
                chns_info.append([asic_dac, chn_pkp, chn_pkn, chn_ped, avg_chns[chn_ploc-20:chn_ploc+80]])
            else:
                chns_info.append([asic_dac, chn_pkp//16, chn_pkn//16, chn_ped//16, avg_chns[chn_ploc-20:chn_ploc+80]//16])
                
        asic_info.append(chns_info)
    return asic_info

def linear_fit(x, y):
    error_fit = False 
    try:
        results = sm.OLS(y,sm.add_constant(x)).fit()
    except ValueError:
        error_fit = True 
    if ( error_fit == False ):
        error_gain = False 
        try:
            slope = results.params[1]
        except IndexError:
            slope = 0
            error_gain = True
        try:
            constant = results.params[0]
        except IndexError:
            constant = 0
    else:
        slope = 0
        constant = 0
        error_gain = True

    y_fit = np.array(x)*slope + constant
    delta_y = abs(y - y_fit)
    inl = delta_y / (max(y)-min(y))
    peakinl = max(inl)
    return slope, constant, peakinl, error_gain

def Chn_Ana(asic_cali, chnno = 0, cap=1.85E-13):
    dacs = []
    ps = []
    ns = []
    peds = []
    wfs  =[]
    for t in asic_cali:
        dacs.append(t[chnno][0])
        ps.append(t[chnno][1])
        ns.append(t[chnno][2])
        peds.append(t[chnno][3])
        wfs.append(t[chnno][4])
    enc_per_v = cap / (1.602E-19)
    enc_daclsb = asic_dac_fit() * enc_per_v
    encs = np.array(dacs)*enc_daclsb
    pos = np.where(encs >= 6250*40)[0][0]
    fit_results = linear_fit(ps[:pos], encs[:pos] )
    oft = int(0-(fit_results[1]/fit_results[0]))
    ps = np.array(ps) - oft + peds[0]
    ns = np.array(ns) + oft - peds[0]

    return encs, ps, ns, peds, wfs, fit_results

def Chn_Plot(asic_cali, chnno = 0, mode16bit=True, fpic = "gain.png"):
    if (mode16bit):
        fs = 65535
    else:
        fs = 4095
    p = Chn_Ana(asic_cali, chnno = chnno)
    
    fig = plt.figure(figsize=(12,4))
    #plt.title("Gain Measurment of Channel %d"%chnno)
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    sps = 20
    for wf in p[4]:
        max_pos = np.where(wf == np.max(wf))[0][0]
        ax1.plot(np.arange(sps)*0.5, wf[max_pos-10: max_pos+10])
        min_pos = np.where(wf == np.min(wf))[0][0]
        ax2.plot(np.arange(sps)*0.5, wf[max_pos+40: max_pos+60])
    ax3.scatter(np.array(p[1]), np.array(p[0])/6250, marker = 'o')
    ax3.scatter(np.array(p[2]), -np.array(p[0])/6250, marker = '*')
    ax3.scatter ([p[3][0]], [0], marker = "s")
    x = np.linspace(0, fs)
    y = (x-p[3][0])*p[5][0]
    ax3.plot( x, y/6250, color ='m', label= "Gain = %d (e-/LSB)\n INL = %.2f%%"%(p[5][0], p[5][2]*100))
    ax3.legend()

    ax1.set_title("Waveforms Overlap of CH%d"%chnno)
    ax2.set_title("Waveforms Overlap of CH%d"%chnno)
    ax3.set_title("Linear Fit of CH%d"%chnno)

    ax1.set_xlabel("Time / $\mu$s")
    ax2.set_xlabel("Time / $\mu$s")
    ax3.set_xlabel("ADC counts / bin")

    ax1.set_ylabel("ADC counts / bin")
    ax2.set_ylabel("ADC counts / bin")
    ax3.set_ylabel("Charge / fC")
    

    ax1.set_xlim((0,10))
    ax2.set_xlim((0,10))
    ax3.set_xlim((0,fs))
   
    ax1.set_ylim((0,fs))
    ax2.set_ylim((0,fs))
    ax3.set_ylim((-100,100))

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    plt.tight_layout()
    plt.savefig( fpic + "_ch%d.png"%chnno)
    plt.close()

testno = 3

for testno in range(1,2):
    tp = "10us"
    sg = "14mVfC"
    testno_str = "Test%02d"%testno
    f_dir = "D:/ColdADC/D2_gainmeas_acq/"
    fr_dir = f_dir + "results/"
    if (os.path.exists(fr_dir)):
        pass
    else:
        try:
            os.makedirs(fr_dir)
        except OSError:
            print ("Error to create folder ")
            exit()
    
    period = 200
    avg_n = 50
    fs = file_list(runpath=f_dir)
    data_fs = []
    for f in fs:
        if (f.find(testno_str)>0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".bin")>0):
            data_fs.append(f)
    
    asic_cali = Asic_Cali(data_fs, mode16bit = True)
    
    fpic = f_dir + f[:f.find("asicdac")]
    chn_gains = []
    chn_inls = []
    for i in range(16):
        Chn_Plot(asic_cali, chnno = i, mode16bit = True, fpic=(fr_dir + testno_str + tp + sg) )
        p = Chn_Ana(asic_cali, chnno = i)
        chn_gains.append(int(p[5][0]))
        chn_inls.append(p[5][2])
    
    csv_fn = fr_dir + testno_str + tp + sg + ".csv"
    with open(csv_fn, "w") as cfp:
        cfp.write(",".join(str(i) for i in chn_gains) +  "," + "\n")
        cfp.write(",".join(str(i) for i in chn_inls) +  "," + "\n")
    
    print (chn_gains)

