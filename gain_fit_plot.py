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

def Asic_Cali(data_fs):
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
            chns_info.append([asic_dac, chn_pkp, chn_pkn, chn_ped, avg_chns[chn_ploc-20:chn_ploc+80]])

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

def Chn_Plot(asic_cali, chnno = 0):
    p = Chn_Ana(asic_cali, chnno = chnno)
    
    fig = plt.figure(figsize=(12,4))
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    sps = 20
    for wf in p[4]:
        max_pos = np.where(wf == np.max(wf))[0][0]
        ax1.plot(np.arange(sps)*0.5, wf[max_pos-10: max_pos+10])
        min_pos = np.where(wf == np.min(wf))[0][0]
        ax2.plot(np.arange(sps)*0.5, wf[min_pos-10: min_pos+10])
    ax3.scatter(np.array(p[1]), np.array(p[0])/6250, marker = 'o')
    ax3.scatter(np.array(p[2]), np.array(p[0])/6250, marker = '*')
    ax3.scatter ([p[3][0]], [0], marker = "s")
    x = np.linspace(p[3][0], p[1][10])
    y = (x-p[3][0])*p[5][0]
    ax3.plot( x, y/6250)

#    ax2 = fig.add_subplot(122)

testno = 1
tp = "10us"
sg = "14mVfC"
testno_str = "Test%02d"%testno
f_dir = "D:/ColdADC/D2_gainmeas_acq/"

period = 200
avg_n = 50
fs = file_list(runpath=f_dir)
data_fs = []
for f in fs:
    if (f.find(testno_str)>0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".bin")>0):
        data_fs.append(f)

asic_cali = Asic_Cali(data_fs)

Chn_Plot(asic_cali, chnno = 0)
#
#fn_pre = "Test%dgainloss_tp10us_sg2_snc0dly"%(testno)
#testno = 1
#chn_sel = 4
#fig = plt.figure(figsize=(12,6))
#ax1 = fig.add_subplot(121)
#ax2 = fig.add_subplot(122)
#
#for fn_pre in ["Test1gainloss_tp10us_sg2_snc0dly", 
#               "Test2gainloss_tp10us_sg2_snc1dly",
#               "Test3gainloss_tp10us_sg2_snc0dly",
#               "Test4gainloss_tp10us_sg2_snc1dly",
#               "Test5gainloss_tp10us_sg2_snc0dly",
#               "Test6gainloss_tp10us_sg2_snc1dly",
#               "Test7gainloss_tp10us_sg2_snc0dly",
#               "Test8gainloss_tp10us_sg2_snc1dly",
#
#               "Test9gainloss_tp10us_sg2_snc0dly",
#               "Test10gainloss_tp10us_sg2_snc1dly",
#               "Test11gainloss_tp10us_sg2_snc0dly",
#               "Test12gainloss_tp10us_sg2_snc1dly",
#               "Test13gainloss_tp10us_sg2_snc0dly",
#               "Test14gainloss_tp10us_sg2_snc1dly",
#               "Test15gainloss_tp10us_sg2_snc0dly",
#               "Test16gainloss_tp10us_sg2_snc1dly",
#
#               ]:
#    dly_avg_chns = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#    for dly in range(0, 50, 1):
#        fn = f_dir + fn_pre + "%02d.bin"%dly
#        with open (fn, 'rb') as fp:
#            chns = pickle.load(fp)
#        oft = 100
#        poft = oft + np.where(np.array(chns[0][oft:])>0xffff)[0][0]
#        avg_chns = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#    
#        avg_n = 50
#        for i in range(0,avg_n):
#            for j in range(len(avg_chns)):
#                if i == 0:
#                    avg_chns[j] = np.array(chns[j][poft+200*i:poft+200+200*i])
#                else:
#                    avg_chns[j] = avg_chns[j] + np.array(chns[j][poft+200*i:poft+200+200*i])
#        for j in range(len(avg_chns)):
#            avg_chns[j] = avg_chns[j]//avg_n
#            dly_avg_chns[j].append( list(avg_chns[j]&0xffff)    )
#    
#    for i in range(len(dly_avg_chns)):
#        tmp = reversed(dly_avg_chns[i])
#        dly_avg_chns[i] = tmp
#                
#
#    dly_chn = [val for tup in zip(*dly_avg_chns[chn_sel]) for val in tup]  
#    sps = (len(dly_chn))
#    x = np.arange(sps)*0.01
#    peak_pos = np.where(dly_chn[0:1000] == np.max(dly_chn[0:1000]))[0][0]
##    ax1.plot(x[0:2000], np.array(dly_chn[peak_pos-200:peak_pos+1800]) - dly_chn[0], label = fn_pre[0:5] )#, marker ='.')
#    if "snc1" in fn_pre:
#        ax2.plot(x[0:2000], np.array(dly_chn[peak_pos-200:peak_pos+1800]) - dly_chn[0], label = fn_pre[0:6])#, marker ='.')
#    else:
#        ax1.plot(x[0:2000], np.array(dly_chn[peak_pos-200:peak_pos+1800]) - dly_chn[0], label = fn_pre[0:6])#, marker ='.')
#ax1.set_xlim([0, 10])
#ax1.set_xlabel("Time / $\mu$s")
#ax1.set_ylim([-5000, 20000])
#ax1.set_ylabel("ADC counts / bin")
#ax1.set_title ("Waveforms with 900mV BL (BL substracted)")
#ax1.grid(True)
#ax1.legend()
#ax2.set_xlim([0, 10])
#ax2.set_xlabel("Time / $\mu$s")
#ax2.set_ylabel("ADC counts / bin")
#ax2.set_ylim([-5000, 20000])
#ax2.set_title ("Waveforms with 200mV BL (BL substracted)")
#ax2.grid(True)
#ax2.legend()
#
#plt.tight_layout()
#plt.savefig("d:/ColdADC/noise/gain_loss_comp.png")
#plt.close()
##plt.show()
#
#
#
